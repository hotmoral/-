package com.receiptledger.v1.document;

public final class ReceiptDocumentDetector {
    public DocumentDetection detect(LumaPlane plane) {
        int w = plane.width();
        int h = plane.height();
        if (w < 32 || h < 32) return DocumentDetection.none("TOO_SMALL");

        double background = cornerMean(plane);
        double interior = mean(plane, w/5, h/5, w*4/5, h*4/5);
        double contrast = interior - background;
        if (Math.abs(contrast) < 18.0) return DocumentDetection.none("LOW_CONTRAST");
        boolean brighter = contrast > 0;
        double threshold = Math.max(12.0, Math.min(60.0, Math.abs(contrast) * 0.30));

        int y0 = Math.max(2, h/20), y1 = Math.min(h-2, h-h/20);
        int x0 = Math.max(2, w/20), x1 = Math.min(w-2, w-w/20);
        double[] leftX = new double[h]; double[] rightX = new double[h]; boolean[] rowOk = new boolean[h];
        double[] topY = new double[w]; double[] bottomY = new double[w]; boolean[] colOk = new boolean[w];
        int rowCount = 0, colCount = 0;

        for (int y = y0; y < y1; y++) {
            int left = firstRun(plane, y, x0, x1, brighter, background, threshold);
            int right = lastRun(plane, y, x0, x1, brighter, background, threshold);
            if (left >= 0 && right > left && right-left >= w/4) {
                leftX[y]=left; rightX[y]=right; rowOk[y]=true; rowCount++;
            }
        }
        for (int x = x0; x < x1; x++) {
            int top = firstRunVertical(plane, x, y0, y1, brighter, background, threshold);
            int bottom = lastRunVertical(plane, x, y0, y1, brighter, background, threshold);
            if (top >= 0 && bottom > top && bottom-top >= h/4) {
                topY[x]=top; bottomY[x]=bottom; colOk[x]=true; colCount++;
            }
        }

        double rowCoverage = rowCount / (double)Math.max(1, y1-y0);
        double colCoverage = colCount / (double)Math.max(1, x1-x0);
        if (rowCoverage < 0.25 || colCoverage < 0.25) return DocumentDetection.none("INSUFFICIENT_BOUNDARY_SUPPORT");

        Line left = fit(rowOk, leftX, y0, y1);
        Line right = fit(rowOk, rightX, y0, y1);
        Line top = fitSwapped(colOk, topY, x0, x1);
        Line bottom = fitSwapped(colOk, bottomY, x0, x1);
        if (left == null || right == null || top == null || bottom == null) return DocumentDetection.none("LINE_FIT_FAILED");

        PointD tl = intersect(left, top);
        PointD tr = intersect(right, top);
        PointD br = intersect(right, bottom);
        PointD bl = intersect(left, bottom);
        if (!finite(tl) || !finite(tr) || !finite(br) || !finite(bl)) return DocumentDetection.none("INTERSECTION_FAILED");

        Quad quad = new Quad(tl, tr, br, bl);
        double areaFraction = quad.area() / (w * (double)h);
        if (!quad.isConvex() || areaFraction < 0.10 || areaFraction > 1.05) return DocumentDetection.none("INVALID_QUAD");
        if (!within(tl,w,h) || !within(tr,w,h) || !within(br,w,h) || !within(bl,w,h)) return DocumentDetection.none("QUAD_OUT_OF_RANGE");

        double contrastScore = Math.min(1.0, Math.abs(contrast) / 80.0);
        double confidence = 0.40*contrastScore + 0.30*Math.min(1,rowCoverage) + 0.30*Math.min(1,colCoverage);
        if (confidence < 0.55) return DocumentDetection.none("LOW_CONFIDENCE");
        return DocumentDetection.found(quad, confidence);
    }

    private static boolean within(PointD p,int w,int h) {
        return p.x >= -0.15*w && p.x <= 1.15*w && p.y >= -0.15*h && p.y <= 1.15*h;
    }
    private static boolean finite(PointD p) { return Double.isFinite(p.x) && Double.isFinite(p.y); }
    private static double cornerMean(LumaPlane p) {
        int pw=Math.max(2,p.width()/10), ph=Math.max(2,p.height()/10);
        return (mean(p,0,0,pw,ph)+mean(p,p.width()-pw,0,p.width(),ph)+mean(p,0,p.height()-ph,pw,p.height())+mean(p,p.width()-pw,p.height()-ph,p.width(),p.height()))/4.0;
    }
    private static double mean(LumaPlane p,int x0,int y0,int x1,int y1) {
        long sum=0; int n=0;
        for(int y=y0;y<y1;y++) for(int x=x0;x<x1;x++){sum+=p.get(x,y);n++;}
        return n==0?0:sum/(double)n;
    }
    private static boolean paper(LumaPlane p,int x,int y,boolean brighter,double bg,double t){int v=p.get(x,y);return brighter?v>=bg+t:v<=bg-t;}
    private static int firstRun(LumaPlane p,int y,int x0,int x1,boolean b,double bg,double t){for(int x=x0;x<x1-2;x++)if(paper(p,x,y,b,bg,t)&&paper(p,x+1,y,b,bg,t)&&paper(p,x+2,y,b,bg,t))return x;return -1;}
    private static int lastRun(LumaPlane p,int y,int x0,int x1,boolean b,double bg,double t){for(int x=x1-1;x>=x0+2;x--)if(paper(p,x,y,b,bg,t)&&paper(p,x-1,y,b,bg,t)&&paper(p,x-2,y,b,bg,t))return x;return -1;}
    private static int firstRunVertical(LumaPlane p,int x,int y0,int y1,boolean b,double bg,double t){for(int y=y0;y<y1-2;y++)if(paper(p,x,y,b,bg,t)&&paper(p,x,y+1,b,bg,t)&&paper(p,x,y+2,b,bg,t))return y;return -1;}
    private static int lastRunVertical(LumaPlane p,int x,int y0,int y1,boolean b,double bg,double t){for(int y=y1-1;y>=y0+2;y--)if(paper(p,x,y,b,bg,t)&&paper(p,x,y-1,b,bg,t)&&paper(p,x,y-2,b,bg,t))return y;return -1;}

    private static Line fit(boolean[] ok,double[] dep,int start,int end){
        double sx=0,sy=0,sxx=0,sxy=0;int n=0;
        for(int i=start;i<end;i++)if(ok[i]){double x=i,y=dep[i];sx+=x;sy+=y;sxx+=x*x;sxy+=x*y;n++;}
        if(n<4)return null;double den=n*sxx-sx*sx;if(Math.abs(den)<1e-9)return null;double a=(n*sxy-sx*sy)/den;double c=(sy-a*sx)/n;return new Line(a,c);
    }
    private static Line fitSwapped(boolean[] ok,double[] dep,int start,int end){
        double sx=0,sy=0,sxx=0,sxy=0;int n=0;
        for(int i=start;i<end;i++)if(ok[i]){double x=i,y=dep[i];sx+=x;sy+=y;sxx+=x*x;sxy+=x*y;n++;}
        if(n<4)return null;double den=n*sxx-sx*sx;if(Math.abs(den)<1e-9)return null;double a=(n*sxy-sx*sy)/den;double c=(sy-a*sx)/n;return new Line(a,c);
    }
    private static PointD intersect(Line xFromY,Line yFromX){
        double den=1.0-yFromX.a*xFromY.a;if(Math.abs(den)<1e-9)return new PointD(Double.NaN,Double.NaN);
        double y=(yFromX.a*xFromY.c+yFromX.c)/den;double x=xFromY.a*y+xFromY.c;return new PointD(x,y);
    }
    private static final class Line { final double a,c; Line(double a,double c){this.a=a;this.c=c;} }
}
