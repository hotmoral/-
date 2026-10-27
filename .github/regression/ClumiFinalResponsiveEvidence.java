package com.example.einsteingame;

import android.app.Dialog;
import android.app.Instrumentation;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.Rect;
import android.graphics.RectF;
import android.os.Bundle;
import android.os.SystemClock;
import android.view.Choreographer;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.GridView;
import android.widget.ScrollView;
import android.widget.TextView;
import java.io.File;
import java.io.FileOutputStream;
import java.io.PrintWriter;
import java.lang.reflect.Field;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import org.json.JSONArray;
import org.json.JSONObject;

/** Final production-screen responsive regression. Test-only, injected by public harness. */
final class ClumiFinalResponsiveEvidence {
    private final Instrumentation host;
    private MainActivity activity;
    private int assertions;
    private final String profile;
    private final JSONObject report=new JSONObject();

    ClumiFinalResponsiveEvidence(Instrumentation host,Bundle args){
        this.host=host;this.profile=args.getString("profile","360x640");
    }

    void run(){
        Bundle result=new Bundle();
        try{
            host.getTargetContext().getSharedPreferences("clumi_progress_v1",0).edit().clear().commit();
            Intent intent=new Intent(host.getTargetContext(),MainActivity.class);
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            activity=(MainActivity)host.startActivitySync(intent);
            settle();

            View root=root();
            check("360x460".equals(profile)||"360x640".equals(profile)||"360x800".equals(profile)||"412x915".equals(profile),"Approved regression profile");
            visible(tagged(root,"home-logo"),"Home logo");
            visible(tagged(root,"home-continue"),"Home primary CTA");
            visible(tagged(root,"home-stage"),"Home stage CTA");
            visible(tagged(root,"home-rewards"),"Home rewards control");
            visible(tagged(root,"home-settings"),"Home settings control");
            textFits(root);shot("01_home");

            click(findButton(root,"스테이지"),"Home Stage");
            root=root();
            visible(tagged(root,"stage-panel"),"Stage panel");
            GridView grid=findType(root,GridView.class);
            check(grid!=null&&grid.getNumColumns()==4&&grid.getAdapter().getCount()==10,"Stage Select 4-column campaign 1-10 grid");
            visible(grid,"Stage grid");
            Button current=findButton(root,"현재 스테이지");
            visible(current,"Current-stage Hero CTA");
            textFits(root);shot("02_stage_select");

            click(current,"Current stage");
            root=root();
            View startPanel=tagged(root,"start-panel");
            Button start=(Button)tagged(root,"stage-cta");
            visible(startPanel,"Stage Start panel");
            visible(start,"Stage Start Hero CTA");
            check(findType(root,ScrollView.class)==null,"Stage Start has no page ScrollView");
            check(start.getText().toString().equals("스테이지 시작"),"Stage Start dynamic Hero CTA text");
            textFits(root);shot("03_stage_start");

            click(start,"Stage Start");
            GameView game=findType(root(),GameView.class);
            check(game!=null&&game.isShown(),"Gameplay canvas loaded");
            gameplayGeometry(game);shot("04_gameplay");

            back();back();back();
            root=root();check(tagged(root,"home-logo")!=null,"Returned to Home");

            click(findByDescription(root,"별 수집"),"Rewards");
            root=root();
            View rewardsPanel=tagged(root,"reward-panel");
            ScrollView rewardList=(ScrollView)tagged(root,"reward-list-scroll");
            View guide=tagged(root,"reward-guide");
            visible(rewardsPanel,"Reward summary");
            visible(rewardList,"Reward scroll viewport");
            visible(guide,"Reward fixed guide");
            check(rewardList.getHeight()>dp(rewardList,36),"Reward list retains usable internal scroll viewport");
            check(rewardList.getParent()!=null&&rewardList.getParent().getClass().getSimpleName().contains("RewardScrollPanel"),"Rewards scroll inside stationary shell");
            textFits(root);shot("05_rewards");

            back();root=root();
            click(findByDescription(root,"설정"),"Settings");
            root=root();
            View shell=tagged(root,"settings-scroll-shell");
            ScrollView settingsScroll=findType(shell,ScrollView.class);
            visible(tagged(root,"brand-header"),"Settings shared header");
            visible(shell,"Settings stationary shell");
            check(settingsScroll!=null&&settingsScroll.getParent()==shell,"Settings content scrolls inside stationary shell");
            check(settingsScroll.getHeight()>dp(settingsScroll,36),"Settings retains usable internal scroll viewport");
            textFits(root);shot("06_settings_light");

            Button dark=findButton(root,"어둡게");
            check(dark!=null,"Dark-mode control exists");
            click(dark,"Dark mode");settleShort();
            root=root();visible(tagged(root,"settings-scroll-shell"),"Dark Settings shell");
            textFits(root);shot("07_settings_dark");

            final Dialog[] resultDialog=new Dialog[1];
            ui(()->resultDialog[0]=ClumiUi.result(activity,1,3,65000L,3,0,"다음 스테이지",()->{},()->{},true));
            settleShort();
            Dialog dialog=resultDialog[0];
            check(dialog!=null&&dialog.isShowing(),"Stage Clear dialog shown");
            View decor=dialog.getWindow().getDecorView();
            View clearPanel=tagged(decor,"clumi-modal-panel");
            View clearStage=tagged(decor,"b3-clear-stage");
            View clearStars=tagged(decor,"b3-clear-stars");
            partlyVisible(clearStage,"Stage Clear stage heading");
            partlyVisible(clearStars,"Stage Clear earned stars");
            check(clearPanel instanceof ViewGroup,"Stage Clear final modal panel is a ViewGroup");
            check(clearStage.getParent()==clearPanel,"Stage Clear heading is hosted directly by the final one-screen panel");
            check(descendsFrom(clearStars,clearPanel),"Stage Clear hero and stars are hosted by the final one-screen panel");
            check(findAncestor(clearStage,ScrollView.class)==null&&findAncestor(clearStars,ScrollView.class)==null,"Stage Clear final content is not hosted by the obsolete ScrollView");
            check(!(clearPanel.getParent() instanceof ScrollView),"Stage Clear panel was reparented out of the construction-time viewport");
            Button clearHome=findButton(decor,"홈"),clearNext=findButton(decor,"다음 스테이지");
            check(clearHome!=null&&clearNext!=null,"Stage Clear actions exist");
            visible(clearHome,"Clear Home action in one-screen composition");
            visible(clearNext,"Clear Next action in one-screen composition");
            textFits(decor);shot("08_clear_dark");
            ui(dialog::dismiss);

            report.put("profile",profile);report.put("assertions",assertions);report.put("status","PASS");writeReport();
            result.putString("stream","Clumi FINAL RESPONSIVE: "+assertions+" assertions PASS ("+profile+")\n");
            host.finish(0,result);
        }catch(Throwable failure){
            try{report.put("profile",profile);report.put("assertions",assertions);report.put("status","FAIL");report.put("error",failure.toString());writeReport();shot("99_failure");}catch(Throwable ignored){}
            java.io.StringWriter detail=new java.io.StringWriter();failure.printStackTrace(new PrintWriter(detail));
            result.putString("stream","Clumi FINAL RESPONSIVE: FAIL ("+profile+")\n"+detail+"\n");host.finish(-1,result);
        }
    }

    private View root(){return activity.getWindow().getDecorView();}
    private void check(boolean value,String message){assertions++;if(!value)throw new AssertionError(message);}
    private void ui(Runnable action){Throwable[] failure=new Throwable[1];host.runOnMainSync(()->{try{action.run();}catch(Throwable t){failure[0]=t;}});if(failure[0]!=null)throw new AssertionError("Android UI action failed",failure[0]);}
    private void frame(){CountDownLatch latch=new CountDownLatch(1);ui(()->Choreographer.getInstance().postFrameCallback(t->latch.countDown()));try{check(latch.await(3,TimeUnit.SECONDS),"Android frame completed");}catch(InterruptedException e){Thread.currentThread().interrupt();throw new AssertionError(e);}}
    private void settle(){
        frame();
        long deadline=SystemClock.elapsedRealtime()+8000;
        while(activity!=null&&activity.navigationInProgress()&&SystemClock.elapsedRealtime()<deadline){SystemClock.sleep(40);ui(()->{});}
        check(activity==null||!activity.navigationInProgress(),"Navigation presentation completed");
        frame();SystemClock.sleep(90);ui(()->{});
    }
    private void settleShort(){frame();SystemClock.sleep(320);ui(()->{});}
    private void back(){ui(activity::onBackPressed);settle();}
    private View tagged(View root,String tag){View v=root.findViewWithTag(tag);check(v!=null,"Tagged component exists: "+tag);return v;}
    private <T extends View>T findType(View root,Class<T> type){if(root==null)return null;if(type.isInstance(root))return type.cast(root);if(root instanceof ViewGroup){ViewGroup g=(ViewGroup)root;for(int i=0;i<g.getChildCount();i++){T v=findType(g.getChildAt(i),type);if(v!=null)return v;}}return null;}
    private <T extends View>T findAncestor(View child,Class<T> type){android.view.ViewParent parent=child==null?null:child.getParent();while(parent instanceof View){if(type.isInstance(parent))return type.cast(parent);parent=parent.getParent();}return null;}
    private boolean descendsFrom(View child,View ancestor){android.view.ViewParent parent=child==null?null:child.getParent();while(parent instanceof View){if(parent==ancestor)return true;parent=parent.getParent();}return false;}
    private Button findButton(View root,String text){if(root instanceof Button&&text.contentEquals(((Button)root).getText()))return (Button)root;if(root instanceof ViewGroup){ViewGroup g=(ViewGroup)root;for(int i=0;i<g.getChildCount();i++){Button v=findButton(g.getChildAt(i),text);if(v!=null)return v;}}return null;}
    private View findByDescription(View root,String description){if(root==null)return null;CharSequence d=root.getContentDescription();if(d!=null&&description.contentEquals(d))return root;if(root instanceof ViewGroup){ViewGroup g=(ViewGroup)root;for(int i=0;i<g.getChildCount();i++){View v=findByDescription(g.getChildAt(i),description);if(v!=null)return v;}}return null;}
    private void click(View view,String label){check(view!=null,label+" control exists");ui(view::performClick);settle();}

    private void visible(View view,String label){
        check(view!=null&&view.isShown(),label+" shown");
        Rect r=new Rect();check(view.getGlobalVisibleRect(r),label+" has global visible rect");
        check(r.width()+2>=view.getWidth()&&r.height()+2>=view.getHeight(),label+" is fully visible, not clipped");
        Bitmap b=host.getUiAutomation().takeScreenshot();
        check(r.left>=0&&r.top>=0&&r.right<=b.getWidth()&&r.bottom<=b.getHeight(),label+" stays inside physical screen");b.recycle();
    }

    private void partlyVisible(View view,String label){
        check(view!=null&&view.isShown(),label+" shown");
        Rect r=new Rect();check(view.getGlobalVisibleRect(r)&&r.width()>0&&r.height()>0,label+" intersects visible viewport");
        Bitmap b=host.getUiAutomation().takeScreenshot();
        check(r.left>=0&&r.top>=0&&r.right<=b.getWidth()&&r.bottom<=b.getHeight(),label+" visible portion stays inside physical screen");b.recycle();
    }

    private Object field(Object target,String name)throws Exception{Field f=target.getClass().getDeclaredField(name);f.setAccessible(true);return f.get(target);}
    private void gameplayGeometry(GameView game)throws Exception{
        float density=game.getResources().getDisplayMetrics().density;
        RectF board=(RectF)field(game,"board"),filters=(RectF)field(game,"filters"),candidates=(RectF)field(game,"candidateFrame"),clue=(RectF)field(game,"cluePanel"),palette=(RectF)field(game,"candidatePanel");
        float boardDp=board.height()/density,clueDp=clue.height()/density;
        // 360x460 is calibrated to the unchanged accepted pre-polish gameplay geometry (7242c767...).
        // This guard detects shrinkage without forcing a redesign of gameplay that this UI closure does not own.
        float minimum="360x460".equals(profile)?185f:"360x640".equals(profile)?300f:330f;
        check(boardDp>=minimum,"Gameplay board retains profile-specific minimum height: "+boardDp+"dp >= "+minimum);
        check(board.height()>candidates.height(),"Board remains visually primary over lower candidate controls");
        check(clue.width()+density>=candidates.width(),"Clue panel receives at least candidate-panel width");
        check(filters.top>board.bottom&&candidates.top>filters.bottom,"Gameplay vertical regions do not overlap");
        check(palette.left>=candidates.left&&palette.right<=candidates.right&&palette.top>=candidates.top&&palette.bottom<=candidates.bottom,"Candidate grid stays inside its frame");
        check(clueDp>=120,"Clue panel remains usable");
        float right=game.getWidth(),bottom=game.getHeight();
        for(RectF r:new RectF[]{board,filters,candidates,clue})check(r.left>=0&&r.top>=0&&r.right<=right&&r.bottom<=bottom,"Gameplay region inside viewport");
        JSONObject g=new JSONObject();g.put("board_height_dp",boardDp);g.put("clue_height_dp",clueDp);g.put("candidate_width_dp",candidates.width()/density);g.put("clue_width_dp",clue.width()/density);report.put("gameplay_geometry",g);
    }

    private void textFits(View view){
        if(view instanceof TextView && !(view instanceof android.widget.Switch) && !(view instanceof android.widget.EditText)){
            TextView t=(TextView)view;
            if(t.getVisibility()==View.VISIBLE&&t.getLayout()!=null&&!t.getText().toString().isEmpty()){
                Object tag=t.getTag();
                boolean baselineRewardTotal="reward-total".equals(tag);
                if(baselineRewardTotal){
                    check(t.getLayout().getLineCount()==1,"Reward total remains one line: "+t.getText());
                }else{
                    int available=t.getHeight()-t.getPaddingTop()-t.getPaddingBottom();
                    check(t.getLayout().getHeight()<=available+3,"Text height fits: "+t.getText());
                }
                if(t instanceof Button)check(t.getLayout().getLineCount()==1,"Button label remains one line: "+t.getText());
            }
        }
        if(view instanceof ViewGroup){ViewGroup g=(ViewGroup)view;for(int i=0;i<g.getChildCount();i++)textFits(g.getChildAt(i));}
    }

    private int dp(View view,float value){return Math.round(value*view.getResources().getDisplayMetrics().density);}
    private File folder(){File f=new File(host.getTargetContext().getExternalFilesDir(null),"final-regression/"+profile);if(!f.exists()&&!f.mkdirs())throw new IllegalStateException("Cannot create evidence folder");return f;}
    private void shot(String name)throws Exception{
        frame();Bitmap b=host.getUiAutomation().takeScreenshot();check(b!=null,"Screenshot captured: "+name);
        String[] parts=profile.split("x");int w=Integer.parseInt(parts[0])*2,h=Integer.parseInt(parts[1])*2;
        check(b.getWidth()==w&&b.getHeight()==h,"Screenshot physical size matches "+profile+": "+b.getWidth()+"x"+b.getHeight());
        try(FileOutputStream out=new FileOutputStream(new File(folder(),name+".png"))){b.compress(Bitmap.CompressFormat.PNG,100,out);}b.recycle();writeBounds(name);
    }
    private void writeBounds(String name)throws Exception{JSONArray a=new JSONArray();collectBounds(root(),a);try(PrintWriter out=new PrintWriter(new File(folder(),name+"-bounds.json"))){out.println(a.toString(2));}}
    private void collectBounds(View view,JSONArray a)throws Exception{
        if(view==null)return;
        if(view.isShown()&&(view.getTag()!=null||view instanceof Button||view instanceof GridView||view instanceof ScrollView)){
            Rect r=new Rect();view.getGlobalVisibleRect(r);float d=view.getResources().getDisplayMetrics().density;
            JSONObject o=new JSONObject();o.put("class",view.getClass().getSimpleName());o.put("tag",view.getTag()==null?"":view.getTag().toString());if(view instanceof TextView)o.put("text",((TextView)view).getText().toString());
            JSONArray box=new JSONArray();box.put(r.left/d);box.put(r.top/d);box.put(r.right/d);box.put(r.bottom/d);o.put("visible_bounds_dp",box);a.put(o);
        }
        if(view instanceof ViewGroup){ViewGroup g=(ViewGroup)view;for(int i=0;i<g.getChildCount();i++)collectBounds(g.getChildAt(i),a);}
    }
    private void writeReport()throws Exception{try(PrintWriter out=new PrintWriter(new File(folder(),"summary.json"))){out.println(report.toString(2));}}
}
