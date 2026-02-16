from moviepy import *
import os
import math

def create_video_v2():
    print("Initializing Video V2 creation...")
    
    # Define durations
    dur_phase1 = 15
    dur_phase2 = 20
    dur_phase3 = 20
    dur_phase4 = 20 
    
    # Load Assets
    asset_dir = 'assets_v2'
    img_data = os.path.join(asset_dir, 'data_preview.png')
    img_code = os.path.join(asset_dir, 'code_view.png')
    img_feat = os.path.join(asset_dir, 'feature_importance.png')
    img_recs = os.path.join(asset_dir, 'clinical_recs.png')
    
    # --- Ken Burns Effect Helper ---
    def ken_burns(clip, start_zoom=1.0, end_zoom=1.1, duration=5):
        # Resize to start zoom
        w, h = clip.size
        
        def effect(get_frame, t):
            # Calculate current zoom level
            zoom = start_zoom + (end_zoom - start_zoom) * (t / duration)
            
            # Get the frame at time t
            img = get_frame(t)
            
            # We can't easily resize per frame in moviepy without being very slow or using PIL
            # A simpler approach for "zoom in" is to resize the clip to end_zoom * resolution at start
            # and then crop a window that shrinks? No, that's zoom out.
            # Zoom IN: Crop a window that shrinks over time from full size to smaller size, then resize back up? 
            # Or resize UP over time and crop center? 
            # MoviePy 'resize' filters are per-frame.
            
            # Let's try a simpler approach: 
            # Resize clip to end_zoom * (1920, 1080) initially? No, memory.
            
            # Standard Ken Burns in MoviePy often uses `scroll` or `resize`. 
            # Let's use a composite transform: 
            # 1. Resize the clip to slightly larger than 1920x1080 (e.g. 1.1x)
            # 2. Extract a 1920x1080 crop that moves lightly? 
            return img 

        # The most robust way in moviepy v2 for a slow zoom:
        # Resize the clip to a large size, then slide a crop wording.
        
        # Method 2: Scale up and center crop.
        # This is computationally expensive per frame. 
        # Let's do a simple PAN (Scroll) instead which is cheaper and looks good.
        # Resize image to width=1920*1.1 = 2112
        large_clip = clip.resized(width=int(1920 * end_zoom))
        
        # Center vertically
        # Scroll horizontally from left to right? or center to slightly off center?
        # Let's scroll from x=0 to x=100
        
        # If we want a zoom, we can use 'resize' with a function of time
        # clip_zoomed = clip.resize(lambda t : 1 + 0.02*t) # linearly zoom
        # But we need to crop to 1920x1080 after resizing.
        
        return clip.resized(lambda t : 1 + (end_zoom - 1) * t / duration) \
                   .with_position('center') # Auto-centers on canvas
        
    def add_motion(img_path, duration):
        # Create clip
        clip = ImageClip(img_path).with_duration(duration)
        
        # Resize to cover screen initially
        # We want to ensure it covers 1920x1080
        # Check aspect ratio
        if clip.w / clip.h > 1920/1080:
             # Image is wider, fit height
             clip = clip.resized(height=1080)
        else:
             # Image is taller or equal, fit width
             clip = clip.resized(width=1920)
             
        # Center it on a 1920x1080 canvas
        clip = CompositeVideoClip([clip.with_position('center')], size=(1920, 1080))
        
        # Apply Zoom (Ken Burns)
        # Zoom from 1.0 to 1.1 over duration
        # We apply the resize function to the COMPOSITE clip so it scales up the whole thing
        zoomed = clip.resized(lambda t : 1 + 0.05 * t / duration) # 5% zoom
        
        # After zooming, we need to crop back to 1920x1080 to avoid growing canvas
        # CompositeVideoClip does not automatically crop unless we tell it
        return zoomed.cropped(x_center=960, y_center=540, width=1920, height=1080)

    # Helper for Text
    def create_text(text, duration, start_time):
        try:
            txt_clip = TextClip(text=text, font_size=45, color='white', font='Arial-Bold', method='caption', size=(1600, None))
        except:
             txt_clip = TextClip(text=text, font_size=45, color='white', method='caption', size=(1600, None))
             
        txt_clip = txt_clip.with_position(('center', 900)).with_duration(duration).with_start(start_time)
        
        # Background: Semi-transparent sleek bar
        # Gradient or solid color? Solid is reliable.
        # Rounded corners? Hard in MoviePy without masks.
        bg_h = txt_clip.h + 50
        bg_clip = ColorClip(size=(1920, int(bg_h)), color=(0,0,0)).with_opacity(0.8)
        bg_clip = bg_clip.with_position(('center', 875)).with_duration(duration).with_start(start_time)
        
        return [bg_clip, txt_clip]

    # --- Phase 1 ---
    print("Processing Phase 1 (Motion)...")
    clip1 = add_motion(img_data, dur_phase1)
    
    subs1 = []
    subs1.extend(create_text("Hospital readmissions are a multi-billion dollar problem.", 5, 0))
    subs1.extend(create_text("Dataset: 100,000+ patient encounters (Diabetes 130-US).", 5, 5))
    subs1.extend(create_text("Goal: Predict high-risk readmissions (< 30 days).", 5, 10))
    
    phase1 = CompositeVideoClip([clip1] + subs1).with_duration(dur_phase1)

    # --- Phase 2 ---
    print("Processing Phase 2 (Motion)...")
    clip2 = add_motion(img_code, dur_phase2)
    
    subs2 = []
    subs2.extend(create_text("ETL Pipeline: Transforming raw CSVs into SQLite.", 7, 0))
    subs2.extend(create_text("Feature Engineering: Mapping 700+ ICD-9 codes.", 7, 7))
    subs2.extend(create_text("Complexity: Calculating Comorbidity Index for each patient.", 6, 14))
    
    phase2 = CompositeVideoClip([clip2] + subs2).with_duration(dur_phase2)

    # --- Phase 3 ---
    print("Processing Phase 3 (Motion)...")
    clip3 = add_motion(img_feat, dur_phase3)
    
    subs3 = []
    subs3.extend(create_text("Model Selection: Random Forest vs. Logistic Regression.", 6, 0))
    subs3.extend(create_text("Logistic Regression selected for Explainability & 55% Recall.", 7, 6))
    subs3.extend(create_text("High Recall is critical to catch at-risk patients.", 7, 13))
    
    phase3 = CompositeVideoClip([clip3] + subs3).with_duration(dur_phase3)

    # --- Phase 4 ---
    print("Processing Phase 4 (Motion)...")
    clip4 = add_motion(img_recs, dur_phase4)
    
    subs4 = []
    subs4.extend(create_text("Key Insight: Prior visits & insulin usage drive risk.", 7, 0))
    subs4.extend(create_text("Action: Deploy screening tool for targeted intervention.", 7, 7))
    subs4.extend(create_text("Outcome: Improved patient care and reduced costs.", 6, 14))
    
    phase4 = CompositeVideoClip([clip4] + subs4).with_duration(dur_phase4)
    
    # --- Assembly with Crossfade ---
    print("Assembling with transitions...")
    # New in v2: concatenate_videoclips has 'padding' or we can manually overlap
    # We will simply CrossFadeIn each clip except the first one? 
    # Or use CompositeVideoClip with start times overlapping?
    
    # standard concatenate doesn't do crossfades easily in one line without 'padding' arg which is negative?
    # Actually, moviepy's CompositeVideoClip is best for crossfades.
    
    # Let's define start times
    t1 = 0
    t2 = t1 + dur_phase1 - 1 # 1 second overlap
    t3 = t2 + dur_phase2 - 1
    t4 = t3 + dur_phase3 - 1
    
    # Apply fadein/fadeout to clips
    # Phase 1: Fade In (0.5), Fade Out (0.5)
    # Actually just CrossFadeIn is enough if we overlap
    
    p1 = phase1.with_start(t1).with_effects([vfx.FadeIn(1)])
    p2 = phase2.with_start(t2).with_effects([vfx.FadeIn(1)])
    p3 = phase3.with_start(t3).with_effects([vfx.FadeIn(1)])
    p4 = phase4.with_start(t4).with_effects([vfx.FadeIn(1)])
    
    # The total duration
    total_duration = t4 + dur_phase4
    
    # Create final composite
    # Note: CompositeVideoClip takes a list of clips.
    # We want them to overlay based on their start times.
    final_video = CompositeVideoClip([p1, p2, p3, p4], size=(1920, 1080)).with_duration(total_duration)
    
    # Write output
    output_path = 'output/hospital_patient_flow_v2.mp4'
    print(f"Writing video to {output_path}...")
    final_video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
    print("Video V2 creation complete!")

if __name__ == "__main__":
    create_video_v2()
