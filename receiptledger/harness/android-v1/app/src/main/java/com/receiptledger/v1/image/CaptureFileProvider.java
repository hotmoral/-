package com.receiptledger.v1.image;

import android.content.ContentProvider;
import android.content.ContentValues;
import android.database.Cursor;
import android.database.MatrixCursor;
import android.net.Uri;
import android.os.ParcelFileDescriptor;
import android.provider.OpenableColumns;

import java.io.File;
import java.io.FileNotFoundException;

public final class CaptureFileProvider extends ContentProvider {
    @Override public boolean onCreate() { return true; }

    @Override public ParcelFileDescriptor openFile(Uri uri, String mode) throws FileNotFoundException {
        File file = resolve(uri);
        int flags;
        if (mode != null && mode.contains("w")) {
            flags = ParcelFileDescriptor.MODE_WRITE_ONLY | ParcelFileDescriptor.MODE_CREATE | ParcelFileDescriptor.MODE_TRUNCATE;
        } else {
            flags = ParcelFileDescriptor.MODE_READ_ONLY;
        }
        return ParcelFileDescriptor.open(file, flags);
    }

    @Override public String getType(Uri uri) { return "image/jpeg"; }

    @Override public Cursor query(Uri uri, String[] projection, String selection, String[] selectionArgs, String sortOrder) {
        File file;
        try { file = resolve(uri); } catch (FileNotFoundException e) { return null; }
        String[] columns = projection == null ? new String[]{OpenableColumns.DISPLAY_NAME, OpenableColumns.SIZE} : projection;
        MatrixCursor cursor = new MatrixCursor(columns, 1);
        Object[] row = new Object[columns.length];
        for (int i=0;i<columns.length;i++) {
            if (OpenableColumns.DISPLAY_NAME.equals(columns[i])) row[i]=file.getName();
            else if (OpenableColumns.SIZE.equals(columns[i])) row[i]=file.length();
            else row[i]=null;
        }
        cursor.addRow(row); return cursor;
    }

    @Override public Uri insert(Uri uri, ContentValues values) { throw new UnsupportedOperationException(); }
    @Override public int update(Uri uri, ContentValues values, String selection, String[] selectionArgs) { return 0; }
    @Override public int delete(Uri uri, String selection, String[] selectionArgs) { return 0; }

    private File resolve(Uri uri) throws FileNotFoundException {
        if (getContext()==null || uri==null || uri.getPathSegments().size()!=1) throw new FileNotFoundException("Invalid capture URI");
        String name=uri.getLastPathSegment();
        if (name==null || !name.matches("[A-Za-z0-9._-]+")) throw new FileNotFoundException("Invalid capture name");
        try {
            File dir=new File(getContext().getCacheDir(),"captures").getCanonicalFile();
            File file=new File(dir,name).getCanonicalFile();
            if (!file.getParentFile().equals(dir)) throw new FileNotFoundException("Path escape rejected");
            return file;
        } catch (java.io.IOException e) {
            FileNotFoundException x=new FileNotFoundException("Capture path unavailable"); x.initCause(e); throw x;
        }
    }
}
