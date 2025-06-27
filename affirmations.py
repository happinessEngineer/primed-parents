import random
from PIL import Image, ImageDraw, ImageFont
import os

affirmations = [
    {"category": "Overwhelm by Information", "affirmation": "You don’t need to know everything—you just need to show up with love."},
    {"category": "Overwhelm by Information", "affirmation": "You can trust yourself more than the next parenting article."},
    {"category": "Overwhelm by Information", "affirmation": "You’re allowed to tune out the noise and tune into your child."},
    {"category": "Overwhelm by Information", "affirmation": "You’re doing better than the internet gives you credit for."},
    {"category": "Overwhelm by Information", "affirmation": "You don’t need to be an expert to be an amazing parent."},
    {"category": "Overwhelm by Information", "affirmation": "You have all the wisdom you need inside of you."},
    {"category": "Overwhelm by Information", "affirmation": "You can learn as you go—there’s no perfect roadmap."},
    {"category": "Overwhelm by Information", "affirmation": "Your child doesn’t need a perfect strategy; they need your steady love."},
    {"category": "Overwhelm by Information", "affirmation": "You can filter out what doesn’t feel right for your family."},
    {"category": "Overwhelm by Information", "affirmation": "You are the calm in a world full of noise."},

    {"category": "Screen Time Guilt", "affirmation": "You are a good parent, even when your child watches a screen."},
    {"category": "Screen Time Guilt", "affirmation": "You can choose balance without perfection."},
    {"category": "Screen Time Guilt", "affirmation": "You are modeling flexibility, not failure."},
    {"category": "Screen Time Guilt", "affirmation": "You can create magical moments before or after screen time."},
    {"category": "Screen Time Guilt", "affirmation": "You are not defined by one parenting choice."},
    {"category": "Screen Time Guilt", "affirmation": "You are raising a child in a digital world, and you're doing your best."},
    {"category": "Screen Time Guilt", "affirmation": "You know when to say yes and when to say enough."},
    {"category": "Screen Time Guilt", "affirmation": "You can release guilt and return to connection."},
    {"category": "Screen Time Guilt", "affirmation": "You’re choosing sanity and survival sometimes—and that’s okay."},
    {"category": "Screen Time Guilt", "affirmation": "You’re still deeply present, even if the screen helps for a little while."},

    {"category": "Working Parent Guilt", "affirmation": "You are showing your child what purpose and dedication look like."},
    {"category": "Working Parent Guilt", "affirmation": "You can work and still be an incredibly loving parent."},
    {"category": "Working Parent Guilt", "affirmation": "Your time together matters more than the total hours."},
    {"category": "Working Parent Guilt", "affirmation": "You are making the most of the time you have."},
    {"category": "Working Parent Guilt", "affirmation": "Your presence is more powerful than your schedule."},
    {"category": "Working Parent Guilt", "affirmation": "You are providing, modeling, and nurturing."},
    {"category": "Working Parent Guilt", "affirmation": "You don’t have to do it all to be enough."},
    {"category": "Working Parent Guilt", "affirmation": "You are allowed to care about your work and your family."},
    {"category": "Working Parent Guilt", "affirmation": "You are not choosing one over the other—you’re choosing both, with love."},
    {"category": "Working Parent Guilt", "affirmation": "Your connection can grow even in small daily moments."},

    {"category": "Fear of Messing Up", "affirmation": "You are not supposed to be perfect—you’re supposed to be human."},
    {"category": "Fear of Messing Up", "affirmation": "Your repair matters more than your mistake."},
    {"category": "Fear of Messing Up", "affirmation": "You can grow alongside your child."},
    {"category": "Fear of Messing Up", "affirmation": "You don’t need to protect your child from every struggle—just walk with them through it."},
    {"category": "Fear of Messing Up", "affirmation": "Your love is their safety net."},
    {"category": "Fear of Messing Up", "affirmation": "You are allowed to be messy and still be deeply good."},
    {"category": "Fear of Messing Up", "affirmation": "You are giving your child tools, not trauma."},
    {"category": "Fear of Messing Up", "affirmation": "You are breaking cycles, even if imperfectly."},
    {"category": "Fear of Messing Up", "affirmation": "You can mess up and still be a safe, steady presence."},
    {"category": "Fear of Messing Up", "affirmation": "You’re doing the work—and that’s what matters most."},

    {"category": "Social Media Comparison", "affirmation": "You are raising your child, not someone else’s."},
    {"category": "Social Media Comparison", "affirmation": "You are not behind—you are exactly where you need to be."},
    {"category": "Social Media Comparison", "affirmation": "You can unplug from comparison and plug into connection."},
    {"category": "Social Media Comparison", "affirmation": "You’re already enough without the filter."},
    {"category": "Social Media Comparison", "affirmation": "You’re allowed to define your own success."},
    {"category": "Social Media Comparison", "affirmation": "You are doing things that matter—even if they don’t show up in a post."},
    {"category": "Social Media Comparison", "affirmation": "You are building something deep and beautiful, not just picture-perfect."},
    {"category": "Social Media Comparison", "affirmation": "You are raising real humans, not content."},
    {"category": "Social Media Comparison", "affirmation": "You are free to admire without comparing."},
    {"category": "Social Media Comparison", "affirmation": "You are the parent your child actually needs—not the one social media shows."},

    {"category": "Burnout and Exhaustion", "affirmation": "You are allowed to rest."},
    {"category": "Burnout and Exhaustion", "affirmation": "You can take breaks without guilt."},
    {"category": "Burnout and Exhaustion", "affirmation": "You are not alone—you are deeply human."},
    {"category": "Burnout and Exhaustion", "affirmation": "You are doing enough, even when you feel depleted."},
    {"category": "Burnout and Exhaustion", "affirmation": "You are worthy of care, too."},
    {"category": "Burnout and Exhaustion", "affirmation": "You are allowed to slow down and receive."},
    {"category": "Burnout and Exhaustion", "affirmation": "You are not the only source of love and support—let others help."},
    {"category": "Burnout and Exhaustion", "affirmation": "You don’t have to carry it all alone."},
    {"category": "Burnout and Exhaustion", "affirmation": "You can pause, breathe, and begin again."},
    {"category": "Burnout and Exhaustion", "affirmation": "You deserve gentleness, even from yourself."},

    {"category": "Emotionally Intense Kids", "affirmation": "You are not failing when your child has big feelings."},
    {"category": "Emotionally Intense Kids", "affirmation": "You can stay grounded even during their storms."},
    {"category": "Emotionally Intense Kids", "affirmation": "You are teaching your child emotional safety by offering it."},
    {"category": "Emotionally Intense Kids", "affirmation": "You can hold space without needing to fix everything."},
    {"category": "Emotionally Intense Kids", "affirmation": "You are helping your child learn emotional regulation—one moment at a time."},
    {"category": "Emotionally Intense Kids", "affirmation": "You are strong enough to stay soft."},
    {"category": "Emotionally Intense Kids", "affirmation": "You don’t need all the answers—you just need to stay connected."},
    {"category": "Emotionally Intense Kids", "affirmation": "You are guiding, not controlling."},
    {"category": "Emotionally Intense Kids", "affirmation": "You are the safe place your child needs."},
    {"category": "Emotionally Intense Kids", "affirmation": "You are doing holy work, even when it’s messy."},

    {"category": "Pressure to Be a Fun Parent", "affirmation": "You don’t have to entertain constantly to be enough."},
    {"category": "Pressure to Be a Fun Parent", "affirmation": "You bring joy just by being yourself."},
    {"category": "Pressure to Be a Fun Parent", "affirmation": "You are fun, even in the quiet ways."},
    {"category": "Pressure to Be a Fun Parent", "affirmation": "You can laugh and play when it feels natural—not forced."},
    {"category": "Pressure to Be a Fun Parent", "affirmation": "You don’t need Pinterest to make magic."},
    {"category": "Pressure to Be a Fun Parent", "affirmation": "You are your child’s favorite person, even without the bells and whistles."},
    {"category": "Pressure to Be a Fun Parent", "affirmation": "You are already enough just as you are."},
    {"category": "Pressure to Be a Fun Parent", "affirmation": "You can say no to more and yes to being present."},
    {"category": "Pressure to Be a Fun Parent", "affirmation": "You create memories in the ordinary moments."},
    {"category": "Pressure to Be a Fun Parent", "affirmation": "You bring fun simply by being engaged."},

    {"category": "Identity Loss", "affirmation": "You are still you—and you are expanding."},
    {"category": "Identity Loss", "affirmation": "You can honor both your needs and theirs."},
    {"category": "Identity Loss", "affirmation": "You are allowed to evolve and rediscover yourself."},
    {"category": "Identity Loss", "affirmation": "You can be a parent and a person."},
    {"category": "Identity Loss", "affirmation": "You are reclaiming parts of yourself with love."},
    {"category": "Identity Loss", "affirmation": "You are worthy of your own attention."},
    {"category": "Identity Loss", "affirmation": "You don’t need to shrink to fit anyone’s expectations."},
    {"category": "Identity Loss", "affirmation": "You can rewrite the story of who you are becoming."},
    {"category": "Identity Loss", "affirmation": "You can be grounded in yourself, even as everything changes."},
    {"category": "Identity Loss", "affirmation": "You are still whole."},

    {"category": "Doubting You're Enough", "affirmation": "You are more than enough."},
    {"category": "Doubting You're Enough", "affirmation": "You are exactly what your child needs."},
    {"category": "Doubting You're Enough", "affirmation": "You are worthy, even on your hardest days."},
    {"category": "Doubting You're Enough", "affirmation": "You can love yourself through the doubts."},
    {"category": "Doubting You're Enough", "affirmation": "You are growing into something beautiful."},
    {"category": "Doubting You're Enough", "affirmation": "You are already doing an incredible job."},
    {"category": "Doubting You're Enough", "affirmation": "You are valued, seen, and loved."},
    {"category": "Doubting You're Enough", "affirmation": "You don’t need to earn your worth—it’s already yours."},
    {"category": "Doubting You're Enough", "affirmation": "You are parenting with heart, and that’s what matters most."},
    {"category": "Doubting You're Enough", "affirmation": "You’ve got this—even if you forget sometimes."}
]

randomized_affirmations = [
    {'category': 'Screen Time Guilt', 'affirmation': 'You are a good parent, even when your child watches a screen.'} ,
    {'category': "Doubting You're Enough", 'affirmation': 'You are already doing an incredible job.'} ,
    {'category': 'Pressure to Be a Fun Parent', 'affirmation': 'You are your child’s favorite person, even without the bells and whistles.'} ,
    {'category': 'Emotionally Intense Kids', 'affirmation': 'You can hold space without needing to fix everything.'} ,
    {'category': "Doubting You're Enough", 'affirmation': 'You are parenting with heart, and that’s what matters most.'} ,
    {'category': 'Fear of Messing Up', 'affirmation': 'You’re doing the work—and that’s what matters most.'} ,
    {'category': "Doubting You're Enough", 'affirmation': 'You are more than enough.'} ,
    {'category': "Doubting You're Enough", 'affirmation': 'You’ve got this—even if you forget sometimes.'} ,
    {'category': 'Fear of Messing Up', 'affirmation': 'You are breaking cycles, even if imperfectly.'} ,
    {'category': "Doubting You're Enough", 'affirmation': 'You are worthy, even on your hardest days.'} ,
    {'category': 'Emotionally Intense Kids', 'affirmation': 'You are helping your child learn emotional regulation—one moment at a time.'} ,
    {'category': 'Screen Time Guilt', 'affirmation': "You are raising a child in a digital world, and you're doing your best."} ,
    {'category': 'Burnout and Exhaustion', 'affirmation': 'You are not alone—you are deeply human.'} ,
    {'category': 'Screen Time Guilt', 'affirmation': 'You are not defined by one parenting choice.'} ,
    {'category': 'Social Media Comparison', 'affirmation': 'You’re already enough without the filter.'} ,
    {'category': 'Overwhelm by Information', 'affirmation': 'You can trust yourself more than the next parenting article.'} ,
    {'category': 'Fear of Messing Up', 'affirmation': 'You are not supposed to be perfect—you’re supposed to be human.'} ,
    {'category': 'Identity Loss', 'affirmation': 'You can rewrite the story of who you are becoming.'} ,
    {'category': 'Overwhelm by Information', 'affirmation': 'You don’t need to be an expert to be an amazing parent.'} ,
    {'category': 'Burnout and Exhaustion', 'affirmation': 'You can take breaks without guilt.'} ,
    {'category': 'Screen Time Guilt', 'affirmation': 'You’re choosing sanity and survival sometimes—and that’s okay.'} ,
    {'category': 'Social Media Comparison', 'affirmation': 'You are doing things that matter—even if they don’t show up in a post.'} ,
    {'category': 'Social Media Comparison', 'affirmation': 'You are free to admire without comparing.'} ,
    {'category': 'Pressure to Be a Fun Parent', 'affirmation': 'You don’t have to entertain constantly to be enough.'} ,
    {'category': 'Pressure to Be a Fun Parent', 'affirmation': 'You are fun, even in the quiet ways.'} ,
    {'category': 'Identity Loss', 'affirmation': 'You can honor both your needs and theirs.'} ,
    {'category': 'Overwhelm by Information', 'affirmation': 'You’re doing better than the internet gives you credit for.'} ,
    {'category': 'Working Parent Guilt', 'affirmation': 'Your presence is more powerful than your schedule.'} ,
    {'category': 'Pressure to Be a Fun Parent', 'affirmation': 'You create memories in the ordinary moments.'} ,
    {'category': 'Emotionally Intense Kids', 'affirmation': 'You are strong enough to stay soft.'} ,
    {'category': 'Working Parent Guilt', 'affirmation': 'You are allowed to care about your work and your family.'} ,
    {'category': 'Fear of Messing Up', 'affirmation': 'You don’t need to protect your child from every struggle—just walk with them through it.'} ,
    {'category': 'Overwhelm by Information', 'affirmation': 'You don’t need to know everything—you just need to show up with love.'} ,
    {'category': 'Fear of Messing Up', 'affirmation': 'You can mess up and still be a safe, steady presence.'} ,
    {'category': 'Fear of Messing Up', 'affirmation': 'Your repair matters more than your mistake.'} ,
    {'category': 'Identity Loss', 'affirmation': 'You are still whole.'} ,
    {'category': 'Overwhelm by Information', 'affirmation': 'You’re allowed to tune out the noise and tune into your child.'} ,
    {'category': 'Overwhelm by Information', 'affirmation': 'Your child doesn’t need a perfect strategy; they need your steady love.'} ,
    {'category': 'Social Media Comparison', 'affirmation': 'You are the parent your child actually needs—not the one social media shows.'} ,
    {'category': 'Identity Loss', 'affirmation': 'You don’t need to shrink to fit anyone’s expectations.'} ,
    {'category': 'Working Parent Guilt', 'affirmation': 'You are not choosing one over the other—you’re choosing both, with love.'} ,
    {'category': 'Emotionally Intense Kids', 'affirmation': 'You are not failing when your child has big feelings.'} ,
    {'category': 'Social Media Comparison', 'affirmation': 'You can unplug from comparison and plug into connection.'} ,
    {'category': 'Pressure to Be a Fun Parent', 'affirmation': 'You don’t need Pinterest to make magic.'} ,
    {'category': 'Fear of Messing Up', 'affirmation': 'You can grow alongside your child.'} ,
    {'category': 'Working Parent Guilt', 'affirmation': 'You are providing, modeling, and nurturing.'} ,
    {'category': 'Emotionally Intense Kids', 'affirmation': 'You don’t need all the answers—you just need to stay connected.'} ,
    {'category': 'Fear of Messing Up', 'affirmation': 'You are allowed to be messy and still be deeply good.'} ,
    {'category': 'Overwhelm by Information', 'affirmation': 'You can filter out what doesn’t feel right for your family.'} ,
    {'category': 'Social Media Comparison', 'affirmation': 'You’re allowed to define your own success.'} ,
    {'category': 'Pressure to Be a Fun Parent', 'affirmation': 'You can say no to more and yes to being present.'} ,
    {'category': 'Working Parent Guilt', 'affirmation': 'Your time together matters more than the total hours.'} ,
    {'category': 'Burnout and Exhaustion', 'affirmation': 'You can pause, breathe, and begin again.'} ,
    {'category': 'Burnout and Exhaustion', 'affirmation': 'You are allowed to slow down and receive.'} ,
    {'category': 'Identity Loss', 'affirmation': 'You are allowed to evolve and rediscover yourself.'} ,
    {'category': 'Emotionally Intense Kids', 'affirmation': 'You are teaching your child emotional safety by offering it.'} ,
    {'category': 'Working Parent Guilt', 'affirmation': 'You are showing your child what purpose and dedication look like.'} ,
    {'category': 'Burnout and Exhaustion', 'affirmation': 'You are not the only source of love and support—let others help.'} ,
    {'category': 'Social Media Comparison', 'affirmation': 'You are building something deep and beautiful, not just picture-perfect.'} ,
    {'category': 'Working Parent Guilt', 'affirmation': 'Your connection can grow even in small daily moments.'} ,
    {'category': 'Working Parent Guilt', 'affirmation': 'You don’t have to do it all to be enough.'} ,
    {'category': "Doubting You're Enough", 'affirmation': 'You are exactly what your child needs.'} ,
    {'category': 'Overwhelm by Information', 'affirmation': 'You have all the wisdom you need inside of you.'} ,
    {'category': 'Identity Loss', 'affirmation': 'You are still you—and you are expanding.'} ,
    {'category': 'Screen Time Guilt', 'affirmation': 'You can release guilt and return to connection.'} ,
    {'category': 'Social Media Comparison', 'affirmation': 'You are raising real humans, not content.'} ,
    {'category': 'Screen Time Guilt', 'affirmation': 'You are modeling flexibility, not failure.'} ,
    {'category': 'Screen Time Guilt', 'affirmation': 'You know when to say yes and when to say enough.'} ,
    {'category': 'Overwhelm by Information', 'affirmation': 'You are the calm in a world full of noise.'} ,
    {'category': 'Fear of Messing Up', 'affirmation': 'You are giving your child tools, not trauma.'} ,
    {'category': 'Identity Loss', 'affirmation': 'You can be grounded in yourself, even as everything changes.'} ,
    {'category': 'Working Parent Guilt', 'affirmation': 'You are making the most of the time you have.'} ,
    {'category': 'Pressure to Be a Fun Parent', 'affirmation': 'You bring fun simply by being engaged.'} ,
    {'category': "Doubting You're Enough", 'affirmation': 'You are valued, seen, and loved.'} ,
    {'category': 'Emotionally Intense Kids', 'affirmation': 'You are doing holy work, even when it’s messy.'} ,
    {'category': 'Burnout and Exhaustion', 'affirmation': 'You deserve gentleness, even from yourself.'} ,
    {'category': 'Identity Loss', 'affirmation': 'You are reclaiming parts of yourself with love.'} ,
    {'category': 'Social Media Comparison', 'affirmation': 'You are raising your child, not someone else’s.'} ,
    {'category': "Doubting You're Enough", 'affirmation': 'You can love yourself through the doubts.'} ,
    {'category': 'Burnout and Exhaustion', 'affirmation': 'You are doing enough, even when you feel depleted.'} ,
    {'category': 'Screen Time Guilt', 'affirmation': 'You’re still deeply present, even if the screen helps for a little while.'} ,
    {'category': 'Burnout and Exhaustion', 'affirmation': 'You are allowed to rest.'} ,
    {'category': 'Pressure to Be a Fun Parent', 'affirmation': 'You bring joy just by being yourself.'} ,
    {'category': 'Working Parent Guilt', 'affirmation': 'You can work and still be an incredibly loving parent.'} ,
    {'category': 'Overwhelm by Information', 'affirmation': 'You can learn as you go—there’s no perfect roadmap.'} ,
    {'category': 'Burnout and Exhaustion', 'affirmation': 'You are worthy of care, too.'} ,
    {'category': 'Identity Loss', 'affirmation': 'You are worthy of your own attention.'} ,
    {'category': 'Identity Loss', 'affirmation': 'You can be a parent and a person.'} ,
    {'category': 'Screen Time Guilt', 'affirmation': 'You can create magical moments before or after screen time.'} ,
    {'category': 'Pressure to Be a Fun Parent', 'affirmation': 'You are already enough just as you are.'} ,
    {'category': 'Fear of Messing Up', 'affirmation': 'Your love is their safety net.'} ,
    {'category': 'Emotionally Intense Kids', 'affirmation': 'You are guiding, not controlling.'} ,
    {'category': 'Pressure to Be a Fun Parent', 'affirmation': 'You can laugh and play when it feels natural—not forced.'} ,
    {'category': 'Emotionally Intense Kids', 'affirmation': 'You can stay grounded even during their storms.'} ,
    {'category': "Doubting You're Enough", 'affirmation': 'You are growing into something beautiful.'} ,
    {'category': 'Emotionally Intense Kids', 'affirmation': 'You are the safe place your child needs.'} ,
    {'category': 'Burnout and Exhaustion', 'affirmation': 'You don’t have to carry it all alone.'} ,
    {'category': 'Screen Time Guilt', 'affirmation': 'You can choose balance without perfection.'} ,
    {'category': "Doubting You're Enough", 'affirmation': 'You don’t need to earn your worth—it’s already yours.'} ,
    {'category': 'Social Media Comparison', 'affirmation': 'You are not behind—you are exactly where you need to be.'} ,
]

bg_colors = [
    (24, 145, 135),    # Medium Aqua Blue
    (110, 80, 170),    # Medium Lavender
    (200, 110, 60),    # Medium Peach/Coral
    (200, 60, 100),    # Medium Rose Pink
    (200, 170, 60),    # Medium Yellow
    (60, 170, 110),    # Medium Mint Green
    (200, 100, 140),   # Medium Pastel Pink
    (70, 130, 180)     # Medium Powder Blue
]

def create_image(text, num):
    output_dir = "affirmation_images"
    
    single_bg_color = bg_colors[num % len(bg_colors)]
    
    # Image dimensions
    width = 1024
    height = 1024
    
    # Font settings
    font_size = 72
    
    # Increased spacing between lines further
    line_spacing = 30 # Increased spacing between lines further
    
    # Sparkle icon settings
    sparkle_image_path = "star.png"
    sparkle_opacity = 0.25 # 25% opacity
    top_right_sparkle_size_multiplier = 0.125 # 1/8 of width
    bottom_left_sparkle_size_multiplier = 0.166 # About 1/6 of width
    edge_padding = 60 # Padding from the image edges
    
    font = ImageFont.truetype("Quicksand-VariableFont_wght.ttf", size=font_size)
    font.set_variation_by_axes([600])  # Set weight to 600 (semi-bold for main text)
    
    # Create new image with background color
    img = Image.new('RGB', (width, height), single_bg_color)
    draw = ImageDraw.Draw(img)
    
    # Add sparkle icons
    try:
        # Load, resize, and set transparency for the top-right sparkle
        sparkle_img_tr = Image.open(sparkle_image_path).convert("RGBA")
        sparkle_size_tr = int(width * top_right_sparkle_size_multiplier)
        sparkle_img_tr = sparkle_img_tr.resize((sparkle_size_tr, sparkle_size_tr), Image.Resampling.LANCZOS)
        alpha_tr = sparkle_img_tr.getchannel('A')
        alpha_tr = alpha_tr.point(lambda i: i * sparkle_opacity)
        sparkle_img_tr.putalpha(alpha_tr)

        # Load, resize, and set transparency for the bottom-left sparkle
        sparkle_img_bl = Image.open(sparkle_image_path).convert("RGBA")
        sparkle_size_bl = int(width * bottom_left_sparkle_size_multiplier)
        sparkle_img_bl = sparkle_img_bl.resize((sparkle_size_bl, sparkle_size_bl), Image.Resampling.LANCZOS)
        alpha_bl = sparkle_img_bl.getchannel('A')
        alpha_bl = alpha_bl.point(lambda i: i * sparkle_opacity)
        sparkle_img_bl.putalpha(alpha_bl)

        # Calculate positions
        sparkle_w_tr, sparkle_h_tr = sparkle_img_tr.size
        sparkle_x_tr = width - sparkle_w_tr - edge_padding
        sparkle_y_tr = edge_padding

        sparkle_w_bl, sparkle_h_bl = sparkle_img_bl.size
        sparkle_x_bl = edge_padding
        sparkle_y_bl = height - sparkle_h_bl - edge_padding

        # Paste sparkles onto the image
        img.paste(sparkle_img_tr, (sparkle_x_tr, sparkle_y_tr), sparkle_img_tr)
        img.paste(sparkle_img_bl, (sparkle_x_bl, sparkle_y_bl), sparkle_img_bl)

    except FileNotFoundError:
        print(f"Warning: Sparkle image not found at {sparkle_image_path}. Skipping sparkles.")
    except Exception as e:
        print(f"An error occurred while processing sparkle image: {e}. Skipping sparkles.")
    
    # Wrap text to fit width
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        text_width = bbox[2] - bbox[0]
        
        if text_width <= width - 100:  # Leave 50px margin on each side
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    # Calculate total text height
    total_height = 0
    line_heights = []
    for line in lines:
        # Calculate line height based on the font that will be used for that segment
        # This is complex as it depends on which parts are quotes.
        # For simplicity, let's approximate using the regular font height for total block height calculation
        bbox = draw.textbbox((0, 0), line, font=font)
        line_height = bbox[3] - bbox[1]
        line_heights.append(line_height)
        total_height += line_height
    
    # Calculate starting y position to center text vertically (including line spacing)
    total_block_height = total_height + (len(lines) - 1) * line_spacing # Total height including spacing
    y = (height - total_block_height) // 2
    
    # Draw each line
    for line in lines:
        # Calculate the starting x position to center the line
        line_width_regular = draw.textbbox((0,0), line, font=font)[2] - draw.textbbox((0,0), line, font=font)[0] # Use regular font for overall centering
        start_x = (width - line_width_regular) // 2
        
        # Draw the entire line in white with the regular font first
        draw.text((start_x, y), line, font=font, fill=(255, 255, 255))
        
        # Move down for the next line
        # Use the approximate line height calculated earlier plus spacing
        current_line_index = lines.index(line) # Get index of current line
        y += line_heights[current_line_index] + line_spacing;
    
    # Add 'Primed Parents' at the bottom
    watermark_font_size = 48
    watermark_font = ImageFont.truetype("Quicksand-VariableFont_wght.ttf", size=watermark_font_size)
    watermark_font.set_variation_by_axes([600])  # Set weight to 600 (semi-bold for main text)
    watermark_text = "Primed Parents"
    watermark_bbox = draw.textbbox((0, 0), watermark_text, font=watermark_font)
    watermark_w = watermark_bbox[2] - watermark_bbox[0]
    watermark_h = watermark_bbox[3] - watermark_bbox[1]
    # Load and resize heart-hands image at double size
    heart_img = Image.open("heart-hands.png").convert("RGBA")
    heart_h = watermark_h * 2
    heart_w = int(heart_img.width * (heart_h / heart_img.height))
    heart_img_resized = heart_img.resize((heart_w, heart_h), Image.Resampling.LANCZOS)
    gap = 18  # move heart closer to text (was 32)

    # Right align: watermark text to the right, heart image to the left of it
    total_w = heart_w + gap + watermark_w
    margin_right = 60
    margin_bottom = 40
    watermark_x = width - total_w - margin_right
    # Move the heart down slightly (e.g., 10px lower than before)
    heart_offset_y = 10
    watermark_y = height - heart_h - margin_bottom + heart_offset_y

    # Paste heart-hands image
    img.paste(heart_img_resized, (watermark_x, watermark_y), heart_img_resized)
    # Draw watermark text after the image
    draw.text((watermark_x + heart_w + gap, watermark_y), watermark_text, font=watermark_font, fill=(255, 255, 255))
    
    # Save image
    output_path = os.path.join(output_dir, f"{num}.jpg")
    img.save(output_path)
    print(f"Created {output_path}")


for idx, affirmation_obj in enumerate(randomized_affirmations):
    print(affirmation_obj, ",")
    affirmation_text = affirmation_obj["affirmation"]
    create_image(affirmation_text, idx)

