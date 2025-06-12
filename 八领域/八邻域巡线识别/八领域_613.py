import cv2
import numpy as np
import math

# 全局变量
prev_angle = None  # 跟踪上一帧的角度
visible_range = 100  # 只显示底部100像素的中线
start_point_l = [0, 0]  # 左边起点的x，y值
start_point_r = [0, 0]  # 右边起点的x，y值
initial_ideal_midline_x = None  # 初始理想中线点
is_initial_ideal_midline_set = False  # 标志位，表示是否已经设置初始理想中线点

# 定义图像大小
image_h = 512  # 图像高度
image_w = 320  # 图像宽度

# 边界跟踪算法实现
# 全局变量
points_l = []     # 左边界的点
points_r = []     # 右边界的点
dir_l = []        # 左边界的生长方向
dir_r = []        # 右边界的生长方向
data_stastics_l = 0  # 左边界的点数统计
data_stastics_r = 0  # 右边界的点数统计
hightest = 0        # 最高点
border_min = 0
border_max = image_w - 1

def get_start_point(bin_image, image_h, image_w, border_min, border_max, start_row):
    """
    寻找两个边界的边界点作为八邻域循环的起始点
    :param bin_image: 二值图像数组
    :param image_h: 图像高度
    :param image_w: 图像宽度
    :param border_min: 边界最小值
    :param border_max: 边界最大值
    :param start_row: 起始行
    :return: 是否找到左右边界点
    """
    start_point_l[0] = 0  # x
    start_point_l[1] = 0  # y

    start_point_r[0] = 0  # x
    start_point_r[1] = 0  # y

    l_found = False
    r_found = False

    # 从中间往左边，先找起点
    for i in range(image_w // 2, border_min - 1, -1):
        if bin_image[start_row][i] == 255 and bin_image[start_row][i - 1] == 0:
            start_point_l[0] = i  # x
            start_point_l[1] = start_row  # y
            l_found = True
            break

    for i in range(image_w // 2, border_max):
        if bin_image[start_row][i] == 255 and bin_image[start_row][i + 1] == 0:
            start_point_r[0] = i  # x
            start_point_r[1] = start_row  # y
            r_found = True
            break

    return l_found and r_found


def search_l_r(bin_image, image_h, image_w, border_min, border_max, break_flag, l_start_x, l_start_y, r_start_x, r_start_y):
    """
    八邻域正式开始找右边点的函数
    :param bin_image: 二值图像数组
    :param image_h: 图像高度
    :param image_w: 图像宽度
    :param border_min: 边界最小值
    :param border_max: 边界最大值
    :param break_flag: 最多循环次数
    :param l_start_x: 左边起点x坐标
    :param l_start_y: 左边起点y坐标
    :param r_start_x: 右边起点x坐标
    :param r_start_y: 右边起点y坐标
    :return: 左右边界数据和最高点
    """
    global points_l, points_r, dir_l, dir_r, data_stastics_l, data_stastics_r, hightest

    points_l = []  # 左线点
    points_r = []  # 右线点
    dir_l = []  # 左边生长方向
    dir_r = []  # 右边生长方向
    data_stastics_l = 0  # 左边找到点的个数
    data_stastics_r = 0  # 右边找到点的个数
    hightest = 0  # 最高点

    # 定义八个邻域
    seeds_l = np.array([[0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1], [1, 0], [1, 1]])
    seeds_r = np.array([[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]])

    center_point_l = [l_start_x, l_start_y]  # 左边中心点
    center_point_r = [r_start_x, r_start_y]  # 右边中心点


    for _ in range(break_flag):
        # 左边八邻域搜索
        search_filds_l = center_point_l + seeds_l
        search_filds_l[:, 0] = np.clip(search_filds_l[:, 0], border_min, border_max)
        search_filds_l[:, 1] = np.clip(search_filds_l[:, 1], 0, image_h - 1)

        temp_l = []
        for i in range(8):
            if (0 <= search_filds_l[i][1] < image_h and border_min <= search_filds_l[i][0] < border_max and
                    bin_image[search_filds_l[i][1]][search_filds_l[i][0]] == 0 and
                    (0 <= search_filds_l[(i + 1) % 8][1] < image_h and border_min <= search_filds_l[(i + 1) % 8][0] < border_max and
                     bin_image[search_filds_l[(i + 1) % 8][1]][search_filds_l[(i + 1) % 8][0]] == 255)):
                temp_l.append(search_filds_l[i].tolist())

        if temp_l:
            dir_l.append(temp_l[0][1] - center_point_l[1])
            points_l.append(center_point_l.copy())
            data_stastics_l += 1
            center_point_l = temp_l[0]

        # 右边八邻域搜索
        search_filds_r = center_point_r + seeds_r
        search_filds_r[:, 0] = np.clip(search_filds_r[:, 0], border_min, border_max)
        search_filds_r[:, 1] = np.clip(search_filds_r[:, 1], 0, image_h - 1)

        temp_r = []
        for i in range(8):
            if (0 <= search_filds_r[i][1] < image_h and border_min <= search_filds_r[i][0] < border_max and
                    bin_image[search_filds_r[i][1]][search_filds_r[i][0]] == 0 and
                    (0 <= search_filds_r[(i + 1) % 8][1] < image_h and border_min <= search_filds_r[(i + 1) % 8][0] < border_max and
                     bin_image[search_filds_r[(i + 1) % 8][1]][search_filds_r[(i + 1) % 8][0]] == 255)):
                temp_r.append(search_filds_r[i].tolist())

        if temp_r:
            dir_r.append(temp_r[0][1] - center_point_r[1])
            points_r.append(center_point_r.copy())
            data_stastics_r += 1
            center_point_r = temp_r[0]

        # 检查是否需要退出循环
        if (len(points_r) >= 3 and points_r[-1][0] == points_r[-2][0] == points_r[-3][0] and
                points_r[-1][1] == points_r[-2][1] == points_r[-3][1]):
            break

        if (len(points_l) >= 3 and points_l[-1][0] == points_l[-2][0] == points_l[-3][0] and
                points_l[-1][1] == points_l[-2][1] == points_l[-3][1]):
            break

        if len(points_r) > 0 and len(points_l) > 0:
            if (abs(points_r[-1][0] - points_l[-1][0]) < 2 and
                    abs(points_r[-1][1] - points_l[-1][1]) < 2):
                hightest = (points_r[-1][1] + points_l[-1][1]) // 2
                break

    return data_stastics_l, data_stastics_r, hightest


def get_left(total_L):
    """
    从八邻域边界里提取需要的左边界线
    :param total_L: 左边界点总数
    :return: 左边界数组
    """
    l_border = [0] * image_h
    for i in range(image_h):
        l_border[i] = border_min

    h = image_h - 2
    for j in range(total_L):
        if 0 <= points_l[j][1] < image_h and points_l[j][1] == h:
            l_border[h] = points_l[j][0] + 1
            h -= 1
            if h == 0:
                break

    return l_border


def get_right(total_R):
    """
    从八邻域边界里提取需要的右边界线
    :param total_R: 右边界点总数
    :return: 右边界数组
    """
    r_border = [0] * image_h
    for i in range(image_h):
        r_border[i] = border_max

    h = image_h - 2
    for j in range(total_R):
        if 0 <= points_r[j][1] < image_h and points_r[j][1] == h:
            r_border[h] = points_r[j][0] - 1
            h -= 1
            if h == 0:
                break

    return r_border

def calculate_midline_offset(l_border, r_border):
    """
    计算理想中线、偏移量、引导线长度和偏差角度
    :param l_border: 左边界数组
    :param r_border: 右边界数组
    :return: 偏移量、引导线长度、偏差角度、中线数组
    """
    # 计算理想中线
    midline = [0] * image_h

    for y in range(image_h):
        if l_border[y] != 0 and r_border[y] != image_w - 1:
            midline[y] = (l_border[y] + r_border[y]) // 2
        else:
            # 如果边界不完整，使用线性插值或默认值
            if y > 0 and midline[y-1] != 0:
                midline[y] = midline[y-1]
            else:
                midline[y] = image_w // 2

    # 获取引导线终点（底部可见区域的中点）
    bottom_y = image_h - 1
    bottom_mid_x = midline[bottom_y]

    global initial_ideal_midline_x, is_initial_ideal_midline_set

    # 设置初始理想中线的底部点（仅在第一次有效检测时）
    if not is_initial_ideal_midline_set:
        initial_ideal_midline_x = bottom_mid_x
        is_initial_ideal_midline_set = True
        print(f"Initial ideal midline point set to: {initial_ideal_midline_x}")

    # 确保 initial_ideal_midline_x 是整数
    if initial_ideal_midline_x is None:
        initial_ideal_midline_x = image_w // 2  # 默认值

    # 计算偏移量、引导线长度和偏差角度
    offset = bottom_mid_x - initial_ideal_midline_x

    # 计算引导线长度（从底部到顶部的中线长度）
    top_y = max(0, image_h - visible_range)
    top_mid_x = midline[top_y]

    midline_length = math.sqrt((bottom_mid_x - top_mid_x) ** 2 + (bottom_y - top_y) ** 2)

    # 避免除以零的情况
    if midline_length == 0:
        midline_length = 1e-6  # 添加一个小的值防止除以零

    # 计算偏差角度（使用反正切函数）
    angle_to_mid_radian = math.atan2(offset, midline_length)

    return offset, midline_length, angle_to_mid_radian, midline


# 初始化摄像头
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Unable to open camera.")
else:
    print("Camera opened successfully.")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Unable to read frame.")
            break

        # 显示原始帧
        frame_copy = frame.copy()  # 创建一个副本用于绘制起始点
        frame_copy = cv2.resize(frame_copy, (320, 512))
        cv2.imshow('Original Frame', frame_copy)

        # 预处理：高斯模糊和颜色过滤
        frame_copy_BGR = cv2.GaussianBlur(frame_copy, (7, 7), 0)
        hsv = cv2.cvtColor(frame_copy_BGR, cv2.COLOR_BGR2HSV)
        # 定义黑色的HSV范围
        colorLow = np.array([0, 0, 0])
        colorHigh = np.array([180, 240, 46])
        mask = cv2.inRange(hsv, colorLow, colorHigh)

        # 形态学操作优化掩膜
        kernal = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernal)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernal)

        # 寻找轮廓
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # 寻找最大轮廓
            largest_contour = max(contours, key=cv2.contourArea)
            largest_mask = np.zeros_like(mask)
            cv2.drawContours(largest_mask, [largest_contour], -1, (255), thickness=cv2.FILLED)
            cv2.imshow('largest mask', largest_mask)

            # 在最大轮廓上应用边界提取函数
            start_row = image_h - 1  # 从底部开始

            # 寻找起始点
            if get_start_point(largest_mask, image_h, image_w, border_min, border_max, start_row):
                l_start_x, l_start_y = start_point_l
                r_start_x, r_start_y = start_point_r

                # 八邻域搜索
                break_flag = 1000  # 最多循环次数
                total_L, total_R, hightest = search_l_r(largest_mask, image_h, image_w, border_min, border_max, break_flag, l_start_x, l_start_y, r_start_x, r_start_y)

                # 提取左右边界
                l_border = get_left(total_L)
                r_border = get_right(total_R)
                
                # 创建一个彩色图像用于绘制边界
                result_image = cv2.cvtColor(largest_mask, cv2.COLOR_GRAY2BGR)
                
                # 新增功能：计算引导线相关信息
                if l_border and r_border:
                    offset, midline_length, angle_to_mid_radian, midline = calculate_midline_offset(l_border, r_border)
                    
                    # 创建一个彩色图像用于绘制边界和中线
                    result_image = cv2.cvtColor(largest_mask, cv2.COLOR_GRAY2BGR)

                    # 只显示底部visible_range像素的边界和中线
                    for y in range(max(0, image_h - visible_range), image_h):
                        if l_border[y] != 0:
                            cv2.circle(result_image, (l_border[y], y), 1, (0, 255, 0), -1)  # 绿色左边界
                        if r_border[y] != image_w - 1:
                            cv2.circle(result_image, (r_border[y], y), 1, (0, 0, 255), -1)  # 红色右边界
                        if midline[y] != 0:
                            cv2.circle(result_image, (midline[y], y), 1, (255, 0, 0), -1)  # 蓝色中线

                    # 获取引导线终点（底部可见区域的中点）
                    bottom_y = image_h - 1
                    bottom_mid_x = midline[bottom_y]
                    top_y = max(0, image_h - visible_range)
                    top_mid_x = midline[top_y]

                    # 计算箭头的终点坐标（朝向引导线的顶部方向）
                    arrow_length = 30
                    arrow_x = int(bottom_mid_x + arrow_length * math.cos(angle_to_mid_radian))
                    arrow_y = int(bottom_mid_x + arrow_length * math.sin(angle_to_mid_radian))

                    # 绘制偏差角度的指示线
                    cv2.line(result_image, (int(bottom_mid_x), bottom_y), (arrow_x, arrow_y), (255, 0, 255), 2)
                    cv2.circle(result_image, (arrow_x, arrow_y), 3, (255, 0, 255), -1)  # 绘制箭头终点

                    # 显示计算结果
                    cv2.putText(result_image, f'Offset: {offset:.2f}px', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    cv2.putText(result_image, f'Length: {midline_length:.2f}px', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    cv2.putText(result_image, f'Angle: {math.degrees(angle_to_mid_radian):.2f}°', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                    # 显示结果
                    cv2.imshow('Boundary Detection', result_image)

                    # 打印结果到控制台
                    print(f"Offset: {offset:.2f}px, Length: {midline_length:.2f}px, Angle: {math.degrees(angle_to_mid_radian):.2f}°")


                # 显示结果
                cv2.imshow('Boundary Detection', result_image)

                # 按'q'键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()