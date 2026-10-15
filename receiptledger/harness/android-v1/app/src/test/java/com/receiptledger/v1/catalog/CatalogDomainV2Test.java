package com.receiptledger.v1.catalog;

import static org.junit.Assert.*;

import com.receiptledger.v1.item.ValueOrigin;
import com.receiptledger.v1.product.CatalogProduct;
import com.receiptledger.v1.product.LinkSource;
import com.receiptledger.v1.product.ProductType;
import com.receiptledger.v1.validation.ValidationStatus;
import org.junit.Test;

public final class CatalogDomainV2Test {
    @Test public void legacyStandardPreservesIdNameTypeWithoutSemanticGuessing() {
        CatalogProduct old = new CatalogProduct("p-legacy-1", ProductType.STANDARD, "서울우유 나100% 1L", 123L);
        CatalogEntryV2 v2 = LegacyCatalogAdapter.fromLegacy(old);
        assertEquals("p-legacy-1", v2.id);
        assertEquals("서울우유 나100% 1L", v2.canonicalName);
        assertEquals(CatalogKind.STANDARD_PRODUCT, v2.kind);
        assertEquals(CatalogEntryV2.RecordOrigin.LEGACY_V1, v2.recordOrigin);
        assertFalse(v2.brand.isPresent());
        assertFalse(v2.productName.isPresent());
        assertFalse(v2.specification.isPresent());
        assertNull(v2.category);
    }

    @Test public void legacyNonStandardBecomesCommodityWithoutInventingUnit() {
        CatalogProduct old = new CatalogProduct("potato", ProductType.NON_STANDARD, "감자", 7L);
        CatalogEntryV2 v2 = LegacyCatalogAdapter.fromLegacy(old);
        assertEquals(CatalogKind.NON_STANDARD_COMMODITY, v2.kind);
        assertEquals("감자", v2.canonicalName);
        assertFalse(v2.specification.isPresent());
    }

    @Test(expected = IllegalArgumentException.class)
    public void unclassifiedCannotBecomeCatalogKind() {
        CatalogKind.fromLegacyClassified(ProductType.UNCLASSIFIED);
    }

    @Test public void stableIdIsOnlyEntityEqualityAuthority() {
        CatalogField<String> brand = CatalogField.userConfirmed("서울우유");
        CatalogField<String> name = CatalogField.userConfirmed("나100%");
        CatalogField<ProductSpecification> spec = CatalogField.userConfirmed(
                new ProductSpecification(new PackageMeasure("1", SalesUnitCode.LITER), 1, null));
        CatalogEntryV2 a = CatalogEntryV2.standard("A", "서울우유 나100% 1L", brand, name,
                CatalogField.absent(), spec, new CategoryRef("milk"), 1L);
        CatalogEntryV2 b = CatalogEntryV2.standard("B", "서울우유 나100% 1L", brand, name,
                CatalogField.absent(), spec, new CategoryRef("milk"), 1L);
        assertNotEquals(a, b);
    }

    @Test public void categoryDoesNotChangeStableIdIdentity() {
        CatalogField<String> name = CatalogField.userConfirmed("테스트제품");
        CatalogEntryV2 a = CatalogEntryV2.standard("same", "테스트제품", CatalogField.absent(), name,
                CatalogField.absent(), CatalogField.absent(), new CategoryRef("cat-a"), 1L);
        CatalogEntryV2 b = CatalogEntryV2.standard("same", "테스트제품", CatalogField.absent(), name,
                CatalogField.absent(), CatalogField.absent(), new CategoryRef("cat-b"), 1L);
        assertEquals(a, b);
        assertNotEquals(a.category, b.category);
    }

    @Test public void highConfidenceParsedFieldIsStillUnconfirmed() {
        CatalogField<String> field = CatalogField.parsed("1L", CatalogField.Confidence.HIGH);
        assertTrue(field.isPresent());
        assertFalse(field.isConfirmed());
        assertEquals(CatalogField.Source.PARSED_FROM_RECEIPT, field.source);
    }

    @Test public void merchantAliasContextsAreIsolated() {
        AliasContext global = AliasContext.global();
        AliasContext a = AliasContext.merchant(" Store A ");
        AliasContext aAgain = AliasContext.merchant("store   a");
        AliasContext b = AliasContext.merchant("STORE B");
        assertEquals(a, aAgain);
        assertNotEquals(global, a);
        assertNotEquals(a, b);
    }

    @Test(expected = IllegalArgumentException.class)
    public void merchantAliasContextRequiresKey() {
        AliasContext.merchant("   ");
    }

    @Test public void packageWeightCanonicalizationIsExact() {
        PackageMeasure kg = new PackageMeasure("1", SalesUnitCode.KILOGRAM);
        PackageMeasure grams = new PackageMeasure("1000", SalesUnitCode.GRAM);
        assertTrue(kg.exactlyEquivalentTo(grams));
        assertEquals(kg.canonicalToken(), grams.canonicalToken());
    }

    @Test public void packageVolumeCanonicalizationIsExact() {
        PackageMeasure liter = new PackageMeasure("1", SalesUnitCode.LITER);
        PackageMeasure ml = new PackageMeasure("1000", SalesUnitCode.MILLILITER);
        assertTrue(liter.exactlyEquivalentTo(ml));
        assertEquals(liter.canonicalToken(), ml.canonicalToken());
    }

    @Test public void packCountsAndUnknownRemainDistinct() {
        ProductSpecification five = new ProductSpecification(null, 5, null);
        ProductSpecification ten = new ProductSpecification(null, 10, null);
        ProductSpecification unknown = ProductSpecification.empty();
        ProductSpecification one = new ProductSpecification(null, 1, null);
        assertNotEquals(five.candidateToken(), ten.candidateToken());
        assertNotEquals(unknown.candidateToken(), one.candidateToken());
    }

    @Test(expected = IllegalArgumentException.class)
    public void packageFormCannotMasqueradeAsNetContentMeasure() {
        new PackageMeasure("1", SalesUnitCode.BAG);
    }

    @Test public void commodityMixedFormsPreserveRawLabelsWithoutNormalizationClaim() {
        CatalogEntryV2 potato = CatalogEntryV2.commodity("c-potato", "감자", new CategoryRef("produce"), 1L);
        assertEquals(CatalogKind.NON_STANDARD_COMMODITY, potato.kind);
        PurchaseForm bag = new PurchaseForm("1", SalesUnitCode.BAG, "봉");
        PurchaseForm kg = new PurchaseForm("1", SalesUnitCode.KILOGRAM, "kg");
        PurchaseForm each = new PurchaseForm("5", SalesUnitCode.EACH, "개");
        PurchaseForm box = new PurchaseForm("1", SalesUnitCode.BOX, "상자");
        assertEquals("봉", bag.rawUnitLabel);
        assertEquals(SalesUnitCode.KILOGRAM, kg.unit);
        assertEquals("5", each.quantity.toPlainString());
        assertEquals("상자", box.rawUnitLabel);
        assertNotEquals(bag.unit, box.unit);
    }

    @Test(expected = IllegalArgumentException.class)
    public void nativeStandardRequiresProductNameField() {
        CatalogEntryV2.standard("x", "제품", CatalogField.absent(), CatalogField.absent(),
                CatalogField.absent(), CatalogField.absent(), null, 1L);
    }

    @Test public void purchaseObservationRetainsEvidenceAndValidationContext() {
        PurchaseForm form = new PurchaseForm("1", SalesUnitCode.PACK, "팩");
        CatalogField<PurchaseForm> formField = CatalogField.of(form,
                CatalogField.Source.RECEIPT_TEXT,
                CatalogField.Confirmation.UNCONFIRMED,
                CatalogField.Confidence.HIGH);
        PurchaseObservationV2 o = new PurchaseObservationV2(
                "r1", 2, "p1", LinkSource.USER_CONFIRMED, "서울우유1000", "2026-10-15", "마트A", 99L,
                formField, ValueOrigin.PRINTED, 2980L, ValueOrigin.PRINTED, 2980L, ValueOrigin.PRINTED,
                ValidationStatus.PASS);
        assertEquals("서울우유1000", o.rawItemName);
        assertEquals("마트A", o.storeName);
        assertEquals("팩", o.purchaseForm.value.rawUnitLabel);
        assertEquals(ValueOrigin.PRINTED, o.unitPriceOrigin);
        assertEquals(LinkSource.USER_CONFIRMED, o.identityLinkSource);
        assertEquals(ValidationStatus.PASS, o.receiptValidation);
    }
}
