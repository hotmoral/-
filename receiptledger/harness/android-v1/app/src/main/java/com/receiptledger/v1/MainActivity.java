package com.receiptledger.v1;

import android.app.Activity;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Intent;
import android.content.pm.ApplicationInfo;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.os.SystemClock;
import android.provider.MediaStore;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;
import com.receiptledger.v1.archive.ReceiptRepository;
import com.receiptledger.v1.design.DesignTokensV1;
import com.receiptledger.v1.design.ResponsiveLayoutPolicyV1;
import com.receiptledger.v1.design.SemanticPresentationV1;
import com.receiptledger.v1.design.SemanticToneV1;
import com.receiptledger.v1.design.UiKitV1;
import com.receiptledger.v1.devicevalidation.DeviceValidationReportV1;
import com.receiptledger.v1.document.DocumentDetection;
import com.receiptledger.v1.document.PerspectivePlan;
import com.receiptledger.v1.document.ProjectiveTransform;
import com.receiptledger.v1.document.Quad;
import com.receiptledger.v1.document.ReceiptDocumentDetector;
import com.receiptledger.v1.image.BitmapLumaAdapter;
import com.receiptledger.v1.image.ImageLoader;
import com.receiptledger.v1.image.PerspectiveWarp;
import com.receiptledger.v1.ocr.OcrDocument;
import com.receiptledger.v1.ocr.OcrGeometryMapper;
import com.receiptledger.v1.persistence.ReceiptRecord;
import com.receiptledger.v1.persistence.ReceiptRecordFactory;
import com.receiptledger.v1.product.SqliteProductCatalogStore;
import com.receiptledger.v1.recovery.OcrRecoveryEngine;
import com.receiptledger.v1.recovery.RecoveryResult;
import com.receiptledger.v1.recovery.RecognitionCandidate;
import com.receiptledger.v1.review.CaptureReviewAssessmentV2;
import com.receiptledger.v1.review.ReceiptReviewDialog;
import com.receiptledger.v1.review.RepeatIdentityReuseV1;
import com.receiptledger.v1.ui.DocumentPreviewView;
import com.receiptledger.v1.ui.SystemBarInsetHelper;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/** Capture/review surface used by the commercial shell; CP37 adds debug-only local validation. */
public final class MainActivity extends Activity {
    private static final int REQ_CAMERA = 1001;
    private static final int REQ_PICK = 1002;

    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private final ReceiptDocumentDetector detector = new ReceiptDocumentDetector();
    private final OcrRecoveryEngine ocrEngine = new OcrRecoveryEngine();
    private final RepeatIdentityReuseV1 repeatReuse = new RepeatIdentityReuseV1();

    private ReceiptRepository repository;
    private SqliteProductCatalogStore catalog;
    private ReceiptRecord pendingRecord;
    private CaptureReviewAssessmentV2 reviewAssessment;
    private DocumentPreviewView preview;
    private LinearLayout stateHost;
    private LinearLayout summaryHost;
    private Button cameraButton;
    private Button galleryButton;
    private Button correctButton;
    private Button originalButton;
    private Button reanalyzeButton;
    private Button reviewButton;
    private Button editAllButton;
    private Button saveButton;
    private Button validationCopyButton;
    private Uri pendingCaptureUri;
    private Bitmap sourceBitmap;
    private Bitmap correctedBitmap;
    private Bitmap displayBitmap;
    private Quad detectedQuad;
    private PerspectivePlan correctedPlan;
    private ProjectiveTransform displayToSource = ProjectiveTransform.identity();
    private DeviceValidationReportV1.AcquisitionSource validationSource =
            DeviceValidationReportV1.AcquisitionSource.UNKNOWN;
    private DeviceValidationReportV1.InitialSnapshot validationInitial;
    private String lastValidationReport;
    private long generation;
    private long displayRevision;

    @Override protected void onCreate(Bundle state) {
        super.onCreate(state);
        repository = new ReceiptRepository(getApplicationContext());
        catalog = new SqliteProductCatalogStore(getApplicationContext());

        LinearLayout outer = new LinearLayout(this);
        outer.setOrientation(LinearLayout.VERTICAL);
        outer.setGravity(Gravity.TOP | Gravity.CENTER_HORIZONTAL);
        UiKitV1.applyPage(this, outer);

        ScrollView scroll = new ScrollView(this);
        scroll.setFillViewport(true);
        outer.addView(scroll, new LinearLayout.LayoutParams(-1, 0, 1f));

        LinearLayout content = new LinearLayout(this);
        content.setOrientation(LinearLayout.VERTICAL);
        scroll.addView(content, new ScrollView.LayoutParams(
                contentWidthPx(), ScrollView.LayoutParams.WRAP_CONTENT,
                Gravity.TOP | Gravity.CENTER_HORIZONTAL));

        content.addView(UiKitV1.title(this, R.string.capture_review_title));
        TextView intro = UiKitV1.body(this, getString(R.string.capture_review_intro));
        content.addView(intro, blockParams(DesignTokensV1.SPACE_2_DP));

        LinearLayout acquire = new LinearLayout(this);
        acquire.setOrientation(LinearLayout.HORIZONTAL);
        cameraButton = UiKitV1.button(this, R.string.capture_camera,
                v -> launchCamera(), UiKitV1.ButtonTone.PRIMARY);
        galleryButton = UiKitV1.button(this, R.string.capture_gallery,
                v -> launchPicker(), UiKitV1.ButtonTone.SECONDARY);
        acquire.addView(cameraButton, weightedButtonParams(false));
        acquire.addView(galleryButton, weightedButtonParams(true));
        content.addView(acquire, blockParams(DesignTokensV1.SPACE_3_DP));

        Button library = UiKitV1.button(this, R.string.capture_library,
                v -> startActivity(new Intent(this, LibraryActivity.class)), UiKitV1.ButtonTone.SECONDARY);
        content.addView(library, blockParams(DesignTokensV1.SPACE_3_DP));

        preview = new DocumentPreviewView(this);
        preview.setMinimumHeight(dp(180));
        content.addView(preview, new LinearLayout.LayoutParams(-1, dp(240)));

        LinearLayout imageActions = new LinearLayout(this);
        imageActions.setOrientation(LinearLayout.HORIZONTAL);
        correctButton = UiKitV1.button(this, R.string.capture_correct,
                v -> correctPerspective(), UiKitV1.ButtonTone.SECONDARY);
        originalButton = UiKitV1.button(this, R.string.capture_original,
                v -> showOriginal(), UiKitV1.ButtonTone.SECONDARY);
        reanalyzeButton = UiKitV1.button(this, R.string.capture_reanalyze,
                v -> runOcr(), UiKitV1.ButtonTone.SECONDARY);
        imageActions.addView(correctButton, weightedButtonParams(false));
        imageActions.addView(originalButton, weightedButtonParams(true));
        imageActions.addView(reanalyzeButton, weightedButtonParams(true));
        content.addView(imageActions, blockParams(DesignTokensV1.SPACE_3_DP));

        stateHost = new LinearLayout(this);
        stateHost.setOrientation(LinearLayout.VERTICAL);
        content.addView(stateHost, blockParams(DesignTokensV1.SPACE_2_DP));
        summaryHost = new LinearLayout(this);
        summaryHost.setOrientation(LinearLayout.VERTICAL);
        content.addView(summaryHost, blockParams(DesignTokensV1.SPACE_2_DP));

        reviewButton = UiKitV1.button(this, R.string.capture_review_required_action,
                v -> reviewRequired(), UiKitV1.ButtonTone.PRIMARY);
        editAllButton = UiKitV1.button(this, R.string.capture_edit_all,
                v -> editAll(), UiKitV1.ButtonTone.SECONDARY);
        saveButton = UiKitV1.button(this, R.string.capture_save,
                v -> saveCurrent(), UiKitV1.ButtonTone.PRIMARY);
        content.addView(reviewButton, blockParams(DesignTokensV1.SPACE_2_DP));
        content.addView(editAllButton, blockParams(DesignTokensV1.SPACE_2_DP));
        content.addView(saveButton, blockParams(0));
        if (isDebuggable()) {
            validationCopyButton = UiKitV1.button(this, R.string.cp37_copy_validation,
                    v -> copyValidationReport(), UiKitV1.ButtonTone.SECONDARY);
            validationCopyButton.setVisibility(View.GONE);
            content.addView(validationCopyButton, blockParams(DesignTokensV1.SPACE_2_DP));
        }

        setContentView(outer);
        SystemBarInsetHelper.apply(this, outer);
        setImageActionsEnabled(false);
        hideReviewActions();
        showState(SemanticPresentationV1.display(
                getString(R.string.capture_ready_title),
                getString(R.string.capture_ready_body),
                SemanticToneV1.INFO));
        worker.execute(() -> repository.reconcileOrphans());
    }

    private void launchCamera() {
        try {
            File dir = new File(getCacheDir(), "captures");
            if (!dir.exists() && !dir.mkdirs()) throw new IOException("capture directory");
            File file = File.createTempFile("receipt_", ".jpg", dir);
            pendingCaptureUri = new Uri.Builder()
                    .scheme("content")
                    .authority(getPackageName() + ".capture")
                    .appendPath(file.getName())
                    .build();
            Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
            intent.putExtra(MediaStore.EXTRA_OUTPUT, pendingCaptureUri);
            intent.addFlags(Intent.FLAG_GRANT_WRITE_URI_PERMISSION | Intent.FLAG_GRANT_READ_URI_PERMISSION);
            intent.setClipData(ClipData.newRawUri("ReceiptLedger capture", pendingCaptureUri));
            if (intent.resolveActivity(getPackageManager()) == null) {
                Toast.makeText(this, R.string.no_camera, Toast.LENGTH_SHORT).show();
                return;
            }
            startActivityForResult(intent, REQ_CAMERA);
        } catch (IOException error) {
            showError(R.string.capture_load_failed_title, error);
        }
    }

    private void launchPicker() {
        Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        intent.setType("image/*");
        intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION);
        startActivityForResult(intent, REQ_PICK);
    }

    @Override protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (resultCode != RESULT_OK) return;
        Uri uri = null;
        if (requestCode == REQ_CAMERA) {
            validationSource = DeviceValidationReportV1.AcquisitionSource.CAMERA;
            uri = pendingCaptureUri;
        } else if (requestCode == REQ_PICK && data != null) {
            validationSource = DeviceValidationReportV1.AcquisitionSource.GALLERY;
            uri = data.getData();
            if (uri != null) {
                try {
                    getContentResolver().takePersistableUriPermission(uri, Intent.FLAG_GRANT_READ_URI_PERMISSION);
                } catch (SecurityException ignored) {
                    // Some providers grant only transient access; the current decode can still proceed.
                }
            }
        }
        if (uri != null) loadImage(uri);
    }

    private void loadImage(Uri uri) {
        long ticket = ++generation;
        displayRevision++;
        invalidateRecord();
        setImageActionsEnabled(false);
        showState(SemanticPresentationV1.display(
                getString(R.string.capture_loading_image_title),
                getString(R.string.capture_loading_image_body),
                SemanticToneV1.INFO));
        worker.execute(() -> {
            try {
                ImageLoader.LoadedImage loaded = ImageLoader.load(this, uri);
                BitmapLumaAdapter.Sampled sampled = BitmapLumaAdapter.sample(loaded.bitmap, 480);
                DocumentDetection detection = detector.detect(sampled.plane);
                Quad quad = detection.found ? sampled.toSource(detection.quad) : null;
                runOnUiThread(() -> {
                    if (ticket != generation) {
                        loaded.bitmap.recycle();
                        return;
                    }
                    if (sourceBitmap != null && sourceBitmap != loaded.bitmap) sourceBitmap.recycle();
                    recycleCorrected();
                    sourceBitmap = loaded.bitmap;
                    correctedPlan = null;
                    detectedQuad = quad;
                    displayBitmap = sourceBitmap;
                    displayToSource = ProjectiveTransform.identity();
                    displayRevision++;
                    preview.setDocument(sourceBitmap, detectedQuad);
                    correctButton.setEnabled(quad != null);
                    originalButton.setEnabled(false);
                    reanalyzeButton.setEnabled(true);
                    runOcr();
                });
            } catch (Exception error) {
                runOnUiThread(() -> {
                    if (ticket == generation) {
                        setImageActionsEnabled(false);
                        showError(R.string.capture_load_failed_title, error);
                    }
                });
            }
        });
    }

    private void correctPerspective() {
        final Bitmap source = sourceBitmap;
        final Quad quad = detectedQuad;
        if (source == null || quad == null) return;
        long ticket = generation;
        invalidateRecord();
        setImageActionsEnabled(false);
        showState(SemanticPresentationV1.display(
                getString(R.string.capture_correcting_title),
                getString(R.string.capture_correcting_body),
                SemanticToneV1.INFO));
        worker.execute(() -> {
            try {
                PerspectiveWarp.Result result = PerspectiveWarp.warp(source, quad);
                runOnUiThread(() -> {
                    if (ticket != generation) {
                        result.bitmap.recycle();
                        return;
                    }
                    recycleCorrected();
                    correctedBitmap = result.bitmap;
                    correctedPlan = result.plan;
                    displayBitmap = correctedBitmap;
                    displayToSource = correctedPlan.outputToSource;
                    displayRevision++;
                    preview.setDocument(correctedBitmap, null);
                    setImageActionsEnabled(true);
                    originalButton.setEnabled(true);
                    runOcr();
                });
            } catch (Exception error) {
                runOnUiThread(() -> {
                    if (ticket == generation) {
                        restoreImageActions();
                        showError(R.string.capture_correction_failed_title, error);
                    }
                });
            }
        });
    }

    private void showOriginal() {
        if (sourceBitmap == null) return;
        invalidateRecord();
        displayBitmap = sourceBitmap;
        displayToSource = ProjectiveTransform.identity();
        displayRevision++;
        preview.setDocument(sourceBitmap, detectedQuad);
        restoreImageActions();
        originalButton.setEnabled(false);
        runOcr();
    }

    private void runOcr() {
        final Bitmap input = displayBitmap;
        if (input == null) return;
        final ProjectiveTransform mapper = displayToSource;
        final long imageTicket = generation;
        final long viewTicket = displayRevision;
        invalidateRecord();
        setImageActionsEnabled(false);
        preview.setOcrQuads(null);
        showState(SemanticPresentationV1.display(
                getString(R.string.capture_processing_title),
                getString(R.string.capture_processing_body),
                SemanticToneV1.INFO));
        final long ocrStartedAt = SystemClock.elapsedRealtime();
        ocrEngine.recognize(input, mapper, new OcrRecoveryEngine.Callback() {
            @Override public void onSuccess(RecoveryResult result) {
                if (imageTicket != generation || viewTicket != displayRevision) return;
                long ocrMillis = Math.max(0L, SystemClock.elapsedRealtime() - ocrStartedAt);
                RecognitionCandidate candidate = result.best;
                preview.setOcrQuads(displayQuads(candidate.document));
                int sourceWidth = sourceBitmap == null ? input.getWidth() : sourceBitmap.getWidth();
                int sourceHeight = sourceBitmap == null ? input.getHeight() : sourceBitmap.getHeight();
                boolean corrected = correctedBitmap != null && displayBitmap == correctedBitmap;
                pendingRecord = ReceiptRecordFactory.create(
                        UUID.randomUUID().toString(),
                        System.currentTimeMillis(),
                        candidate.document,
                        candidate.structure,
                        candidate.items,
                        candidate.validation,
                        sourceWidth,
                        sourceHeight,
                        corrected);
                CaptureReviewAssessmentV2 initialAssessment = CaptureReviewAssessmentV2.assess(pendingRecord);
                validationInitial = DeviceValidationReportV1.captureInitial(
                        validationSource,
                        ocrMillis,
                        result.attemptedPasses(),
                        result.derivedCandidates(),
                        candidate.pass == null ? "UNKNOWN" : candidate.pass.name(),
                        pendingRecord,
                        initialAssessment);
                restoreImageActions();
                updateReviewUi();
            }

            @Override public void onFailure(Exception error) {
                if (imageTicket != generation || viewTicket != displayRevision) return;
                restoreImageActions();
                showError(R.string.capture_ocr_failed_title, error);
            }
        });
    }

    private List<Quad> displayQuads(OcrDocument document) {
        List<Quad> out = new ArrayList<>();
        for (Quad quad : document.sourceElementQuads()) {
            if (displayBitmap == correctedBitmap && correctedPlan != null) {
                out.add(OcrGeometryMapper.map(quad, correctedPlan.sourceToOutput));
            } else {
                out.add(quad);
            }
        }
        return out;
    }

    private void updateReviewUi() {
        ReceiptRecord record = pendingRecord;
        if (record == null) {
            hideReviewActions();
            return;
        }
        reviewAssessment = CaptureReviewAssessmentV2.assess(record);
        showState(SemanticPresentationV1.validation(record.validationStatus));
        summaryHost.removeAllViews();

        if (record.items.isEmpty()) {
            summaryHost.addView(UiKitV1.semanticCard(this, SemanticPresentationV1.display(
                    getString(R.string.capture_no_items_title),
                    getString(R.string.capture_no_items_body),
                    SemanticToneV1.REVIEW)));
            reviewButton.setVisibility(View.GONE);
            editAllButton.setVisibility(View.GONE);
            saveButton.setVisibility(View.VISIBLE);
            saveButton.setEnabled(false);
            return;
        }

        if (reviewAssessment.requiresReview()) {
            summaryHost.addView(UiKitV1.semanticCard(this, SemanticPresentationV1.display(
                    getString(R.string.capture_review_needed_title),
                    getString(R.string.capture_review_needed_body,
                            reviewAssessment.autoConfirmedItems,
                            reviewAssessment.reviewItemCount(),
                            reviewAssessment.receiptFields.size()),
                    SemanticToneV1.REVIEW)));
            reviewButton.setVisibility(View.VISIBLE);
            reviewButton.setEnabled(true);
            editAllButton.setVisibility(View.VISIBLE);
            editAllButton.setEnabled(true);
            saveButton.setVisibility(View.VISIBLE);
            saveButton.setEnabled(false);
        } else {
            summaryHost.addView(UiKitV1.semanticCard(this, SemanticPresentationV1.display(
                    getString(R.string.capture_auto_confirmed_title),
                    getString(R.string.capture_auto_confirmed_body, reviewAssessment.autoConfirmedItems),
                    SemanticToneV1.POSITIVE)));
            reviewButton.setVisibility(View.GONE);
            editAllButton.setVisibility(View.VISIBLE);
            editAllButton.setEnabled(true);
            saveButton.setVisibility(View.VISIBLE);
            saveButton.setEnabled(true);
        }
    }

    private void reviewRequired() {
        ReceiptRecord base = pendingRecord;
        CaptureReviewAssessmentV2 assessment = reviewAssessment;
        if (base == null || assessment == null || !assessment.requiresReview()) return;
        ReceiptReviewDialog.showRequired(this, base, assessment, reviewed -> {
            if (pendingRecord != base) return;
            pendingRecord = reviewed;
            updateReviewUi();
        });
    }

    private void editAll() {
        ReceiptRecord base = pendingRecord;
        if (base == null) return;
        CaptureReviewAssessmentV2 assessment = reviewAssessment == null
                ? CaptureReviewAssessmentV2.assess(base) : reviewAssessment;
        ReceiptReviewDialog.showAll(this, base, assessment, reviewed -> {
            if (pendingRecord != base) return;
            pendingRecord = reviewed;
            updateReviewUi();
        });
    }

    private void saveCurrent() {
        final ReceiptRecord record = pendingRecord;
        final Bitmap image = sourceBitmap;
        final CaptureReviewAssessmentV2 assessment = reviewAssessment;
        final DeviceValidationReportV1.InitialSnapshot validationSnapshot = validationInitial;
        if (record == null || image == null || assessment == null || assessment.requiresReview()) return;
        cameraButton.setEnabled(false);
        galleryButton.setEnabled(false);
        setImageActionsEnabled(false);
        reviewButton.setEnabled(false);
        editAllButton.setEnabled(false);
        saveButton.setEnabled(false);
        showState(SemanticPresentationV1.display(
                getString(R.string.capture_saving_title),
                getString(R.string.capture_saving_body),
                SemanticToneV1.INFO));

        worker.execute(() -> {
            try {
                repository.save(record, image);
            } catch (Exception error) {
                runOnUiThread(() -> {
                    cameraButton.setEnabled(true);
                    galleryButton.setEnabled(true);
                    restoreImageActions();
                    if (pendingRecord == record) {
                        updateReviewUi();
                        showError(R.string.capture_save_failed_title, error);
                    }
                });
                return;
            }

            String builtValidationReport = null;
            if (isDebuggable() && validationSnapshot != null) {
                try {
                    builtValidationReport = DeviceValidationReportV1.savedReport(validationSnapshot, record);
                } catch (RuntimeException ignored) {
                    // Validation reporting is non-authoritative and must never turn a durable save into failure.
                }
            }
            final String savedValidationReport = builtValidationReport;
            RepeatIdentityReuseV1.Result reuse = repeatReuse.apply(record,
                    (receiptId, ordinal, rawName) ->
                            catalog.resolveAndLinkExact(receiptId, ordinal, rawName).classified());
            runOnUiThread(() -> {
                cameraButton.setEnabled(true);
                galleryButton.setEnabled(true);
                restoreImageActions();
                if (pendingRecord == record) {
                    pendingRecord = null;
                    reviewAssessment = null;
                    validationInitial = null;
                    summaryHost.removeAllViews();
                    hideReviewActions();
                    showState(SemanticPresentationV1.display(
                            getString(R.string.capture_saved_title),
                            getString(R.string.capture_saved_body, reuse.linkedCount),
                            SemanticToneV1.POSITIVE));
                    showValidationReport(savedValidationReport);
                }
            });
        });
    }

    private void copyValidationReport() {
        if (lastValidationReport == null || validationCopyButton == null) return;
        ClipboardManager clipboard = (ClipboardManager) getSystemService(CLIPBOARD_SERVICE);
        if (clipboard == null) return;
        clipboard.setPrimaryClip(ClipData.newPlainText("ReceiptLedger CP37", lastValidationReport));
        Toast.makeText(this, R.string.cp37_validation_copied, Toast.LENGTH_SHORT).show();
    }

    private void showValidationReport(String report) {
        lastValidationReport = report;
        if (validationCopyButton == null) return;
        boolean available = report != null && !report.isEmpty();
        validationCopyButton.setVisibility(available ? View.VISIBLE : View.GONE);
        validationCopyButton.setEnabled(available);
    }

    private void clearValidationReport() {
        validationInitial = null;
        lastValidationReport = null;
        if (validationCopyButton != null) validationCopyButton.setVisibility(View.GONE);
    }

    private boolean isDebuggable() {
        return (getApplicationInfo().flags & ApplicationInfo.FLAG_DEBUGGABLE) != 0;
    }

    private void invalidateRecord() {
        ocrEngine.cancelPending();
        pendingRecord = null;
        reviewAssessment = null;
        clearValidationReport();
        if (summaryHost != null) summaryHost.removeAllViews();
        hideReviewActions();
    }

    private void hideReviewActions() {
        if (reviewButton != null) reviewButton.setVisibility(View.GONE);
        if (editAllButton != null) editAllButton.setVisibility(View.GONE);
        if (saveButton != null) saveButton.setVisibility(View.GONE);
    }

    private void setImageActionsEnabled(boolean enabled) {
        if (correctButton != null) correctButton.setEnabled(enabled && detectedQuad != null);
        if (originalButton != null) originalButton.setEnabled(enabled && correctedBitmap != null);
        if (reanalyzeButton != null) reanalyzeButton.setEnabled(enabled && displayBitmap != null);
    }

    private void restoreImageActions() {
        setImageActionsEnabled(displayBitmap != null);
    }

    private void showState(SemanticPresentationV1.Presentation presentation) {
        stateHost.removeAllViews();
        stateHost.addView(UiKitV1.semanticCard(this, presentation), new LinearLayout.LayoutParams(-1, -2));
    }

    private void showError(int titleRes, Exception error) {
        String detail = error == null || error.getMessage() == null || error.getMessage().trim().isEmpty()
                ? getString(R.string.capture_error_generic)
                : error.getMessage();
        showState(SemanticPresentationV1.display(
                getString(titleRes),
                getString(R.string.capture_error_body, detail),
                SemanticToneV1.ERROR));
    }

    private LinearLayout.LayoutParams blockParams(int topDp) {
        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(-1, -2);
        if (topDp > 0) params.topMargin = dp(topDp);
        return params;
    }

    private LinearLayout.LayoutParams weightedButtonParams(boolean marginStart) {
        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(0, -2, 1f);
        if (marginStart) params.setMarginStart(dp(DesignTokensV1.SPACE_2_DP));
        return params;
    }

    private int contentWidthPx() {
        int widthDp = getResources().getConfiguration().screenWidthDp;
        if (widthDp < 1) {
            widthDp = Math.max(1, Math.round(
                    getResources().getDisplayMetrics().widthPixels
                            / getResources().getDisplayMetrics().density));
        }
        int gutter = ResponsiveLayoutPolicyV1.pageGutterDp(widthDp);
        int available = Math.max(dp(240),
                getResources().getDisplayMetrics().widthPixels - dp(gutter * 2));
        return Math.min(available, dp(ResponsiveLayoutPolicyV1.contentMaxWidthDp()));
    }

    private void recycleCorrected() {
        if (correctedBitmap != null && !correctedBitmap.isRecycled()) correctedBitmap.recycle();
        correctedBitmap = null;
    }

    private int dp(int value) {
        return UiKitV1.dp(this, value);
    }

    @Override protected void onDestroy() {
        generation++;
        displayRevision++;
        worker.shutdownNow();
        ocrEngine.close();
        if (catalog != null) catalog.close();
        if (repository != null) repository.close();
        recycleCorrected();
        if (sourceBitmap != null && !sourceBitmap.isRecycled()) sourceBitmap.recycle();
        super.onDestroy();
    }
}
