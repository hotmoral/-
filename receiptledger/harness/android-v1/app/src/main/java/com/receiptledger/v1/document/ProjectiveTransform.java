package com.receiptledger.v1.document;

public final class ProjectiveTransform {
    private final double[] m;

    private ProjectiveTransform(double[] m) {
        this.m = m;
    }

    public static ProjectiveTransform fromQuadToRect(Quad source, int width, int height) {
        PointD[] s = source.points();
        PointD[] d = {
                new PointD(0, 0),
                new PointD(width - 1.0, 0),
                new PointD(width - 1.0, height - 1.0),
                new PointD(0, height - 1.0)
        };
        return fromFourPoints(s, d);
    }

    public static ProjectiveTransform fromFourPoints(PointD[] source, PointD[] destination) {
        if (source == null || destination == null || source.length != 4 || destination.length != 4) {
            throw new IllegalArgumentException("Four source and destination points are required");
        }
        double[][] a = new double[8][9];
        for (int i = 0; i < 4; i++) {
            double x = source[i].x;
            double y = source[i].y;
            double u = destination[i].x;
            double v = destination[i].y;
            int r = i * 2;
            a[r][0] = x; a[r][1] = y; a[r][2] = 1;
            a[r][6] = -u * x; a[r][7] = -u * y; a[r][8] = u;
            a[r + 1][3] = x; a[r + 1][4] = y; a[r + 1][5] = 1;
            a[r + 1][6] = -v * x; a[r + 1][7] = -v * y; a[r + 1][8] = v;
        }
        double[] h = solve(a);
        return new ProjectiveTransform(new double[] {
                h[0], h[1], h[2],
                h[3], h[4], h[5],
                h[6], h[7], 1.0
        });
    }

    public PointD map(PointD p) {
        double w = m[6] * p.x + m[7] * p.y + m[8];
        if (Math.abs(w) < 1e-12) throw new IllegalStateException("Projective point at infinity");
        return new PointD(
                (m[0] * p.x + m[1] * p.y + m[2]) / w,
                (m[3] * p.x + m[4] * p.y + m[5]) / w);
    }

    public ProjectiveTransform inverse() {
        double a=m[0], b=m[1], c=m[2], d=m[3], e=m[4], f=m[5], g=m[6], h=m[7], i=m[8];
        double det = a*(e*i-f*h) - b*(d*i-f*g) + c*(d*h-e*g);
        if (Math.abs(det) < 1e-12) throw new IllegalStateException("Singular projective transform");
        double inv = 1.0 / det;
        return new ProjectiveTransform(new double[] {
                (e*i-f*h)*inv, (c*h-b*i)*inv, (b*f-c*e)*inv,
                (f*g-d*i)*inv, (a*i-c*g)*inv, (c*d-a*f)*inv,
                (d*h-e*g)*inv, (b*g-a*h)*inv, (a*e-b*d)*inv
        });
    }

    public double[] values() {
        return m.clone();
    }

    private static double[] solve(double[][] a) {
        int n = 8;
        for (int col = 0; col < n; col++) {
            int pivot = col;
            for (int row = col + 1; row < n; row++) {
                if (Math.abs(a[row][col]) > Math.abs(a[pivot][col])) pivot = row;
            }
            if (Math.abs(a[pivot][col]) < 1e-12) throw new IllegalArgumentException("Degenerate point configuration");
            double[] tmp = a[col]; a[col] = a[pivot]; a[pivot] = tmp;
            double div = a[col][col];
            for (int j = col; j <= n; j++) a[col][j] /= div;
            for (int row = 0; row < n; row++) {
                if (row == col) continue;
                double factor = a[row][col];
                for (int j = col; j <= n; j++) a[row][j] -= factor * a[col][j];
            }
        }
        double[] out = new double[n];
        for (int i = 0; i < n; i++) out[i] = a[i][n];
        return out;
    }
}
