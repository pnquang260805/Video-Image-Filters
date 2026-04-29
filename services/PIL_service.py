from PIL import Image, ImageFont, ImageDraw
import numpy as np
import cv2

def open_image(image_path : str) -> Image:
    return Image.open(image_path).convert('L')

def get_average_L(image : Image):

    """
    Given PIL Image, return average value of grayscale value
    """
    img = np.array(image)
    w, h = img.shape
    return np.average(img.reshape(w*h))

def convert_to_ascii(image: Image, ascii_chars: str, cols=50, scale=0.43):

    """
    Logic
    Bước 1 — Tính kích thước mỗi ô (tile)
        Ảnh gốc được chia thành một lưới ô nhỏ. Chiều rộng mỗi ô w = W / cols — tức là chia đều chiều ngang ảnh cho số cột mong muốn. 
        Chiều cao h = w / scale không phải tùy ý, mà được tính theo tỉ lệ để bù trừ cho thực tế ký tự ASCII cao hơn rộng (thường scale ≈ 0.43). 
        Nếu không làm vậy, ảnh ASCII sẽ bị kéo dài theo chiều dọc. Số hàng rows tự động suy ra từ đó.

    Bước 2 — Kiểm tra ảnh có đủ lớn không
        Nếu số cột yêu cầu lớn hơn số pixel ngang, hoặc số hàng lớn hơn số pixel dọc, thì mỗi ô sẽ nhỏ hơn 1 pixel — không thể lấy thông tin gì được nữa. 
        Chương trình dừng sớm để tránh kết quả vô nghĩa.
    
    Bước 3 — Lặp qua từng hàng, từng cột
        Đây là vòng lặp lồng nhau duyệt từng ô một theo thứ tự trái→phải, trên→dưới — giống cách mắt người đọc văn bản. 
        Mỗi ô được xác định bởi tọa độ (x1, y1, x2, y2) trên ảnh gốc.

    Bước 4 — Cắt ô ảnh (crop)
        Dùng image.crop() của PIL để cắt đúng vùng pixel tương ứng với ô đang xét. Một chi tiết nhỏ nhưng quan trọng: 
        ô cuối cùng của mỗi hàng được chỉnh x2 = W thay vì (i+1)*w, vì phép chia số nguyên có thể làm mất vài pixel ở rìa phải ảnh.

    Bước 5 — Tính độ sáng trung bình
        Hàm get_average_L() lấy giá trị luminance trung bình của toàn bộ pixel trong ô, trả về một số từ 0 (tối hoàn toàn) đến 255 (sáng hoàn toàn). 
        Toàn bộ màu sắc và chi tiết của ô được "cô đọng" thành một con số duy nhất.
    
    Bước 6 — Tra bảng ký tự ASCII
    """
    # If image is a numpy array (from OpenCV), convert it to PIL Image
    if isinstance(image, np.ndarray):
        # Convert BGR to Grayscale
        if len(image.shape) == 3:
            image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
        else:
            image = Image.fromarray(image)

    W, H = image.size[0], image.size[1]
    grid_w = W / cols
    grid_h = grid_w / scale
    rows = int(H / grid_h)

    if cols > W or rows > H:
        print("Image too small for specified cols!")
        exit(0)
    
    res = []
    for row_idx in range(rows):
        # Tọa độ Y (theo hàng)
        y1 = int(row_idx * grid_h)
        y2 = int((row_idx + 1) * grid_h) if row_idx != rows - 1 else H
        
        line = ""
        for col_idx in range(cols):
            # Tọa độ X (theo cột)
            x1 = int(col_idx * grid_w)
            x2 = int((col_idx + 1) * grid_w) if col_idx != cols - 1 else W
        
            # Kiểm tra tránh vùng crop rỗng
            if x2 <= x1 or y2 <= y1:
                line += ascii_chars[0]
                continue

            crop_image = image.crop((x1, y1, x2, y2))
            avg_luminance = get_average_L(crop_image)

            # Chuyển độ sáng sang ký tự ASCII
            char_idx = int(avg_luminance * (len(ascii_chars) - 1) / 255)
            line += ascii_chars[char_idx]
            
        res.append(line)
    
    return res

def ascii_to_image(ascii_list):
    """
    Render a list of ASCII strings into a numpy image (uint8).
    """
    if not ascii_list:
        return np.zeros((100, 100), dtype=np.uint8)

    try:
        # Chọn font chữ cỡ 12
        font = ImageFont.truetype("consola.ttf", 12)
    except:
        font = ImageFont.load_default()

    char_w, char_h = 7, 12 # Ước lượng kích thước 1 ký tự
    
    rows = len(ascii_list)
    cols = len(ascii_list[0])
    
    img_w = cols * char_w # Chiều rộng ảnh = số cột * độ rộng 1 ký tự
    img_h = rows * char_h # Chiều cao ảnh = số hàng * độ cao 1 ký tự
    
    # Tạo "tờ giấy" trắng (ảnh đen)
    pil_img = Image.new('L', (img_w, img_h), color=0) # Tạo một ảnh mới ở chế độ Grayscale (8-bit màu xám). color=0 Đặt nền là màu đen hoàn
    draw = ImageDraw.Draw(pil_img)
    
    # Draw text
    y_offset = 0
    for line in ascii_list:
        draw.text((0, y_offset), line, font=font, fill=255) # Vẽ dòng chữ màu trắng (255)
        y_offset += char_h #  Xuống dòng bằng cách tăng tọa độ Y
        
    return np.array(pil_img)