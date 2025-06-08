import cv2
import numpy as np

# 全局变量
start_point_l = [0, 0]  # 左边起点的x，y值
start_point_r = [0, 0]  # 右边起点的x，y值


# 定义图像大小
image_h = 512  # 图像高度
image_w = 320  # 图像宽度

#颜色阈值HSV
colorLow = np.array([0, 0, 200])
colorHigh = np.array([180, 30, 255])

# 边界跟踪算法实现
# 全局变量
points_l = []     # 左边界的点
points_r = []     # 右边界的点
dir_l = []        # 左边界的生长方向
dir_r = []        # 右边界的生长方向
data_stastics_l = 0  # 左边界的点数统计
data_stastics_r = 0  # 右边界的点数统计
hightest = 0        # 最高点
start_point_l = [0, 0]  # 左边起点的x，y值
start_point_r = [0, 0]  # 右边起点的x，y值
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

# 计算中间线
def get_center_line(left_border, right_border):
    """
    计算中间线
    :param left_border: 左边界数组
    :param right_border: 右边界数组
    :return: 中间线数组
    """
    center_line = []
    for y in range(image_h):
        if left_border[y] != border_min and right_border[y] != border_max:
            center_x = (left_border[y] + right_border[y]) // 2
            center_line.append((center_x, y))
        else:
            center_line.append(None)  # 如果左右边界中有一个不存在，则中间线也不存在
    return center_line


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
        hsv = cv2.cvtColor( frame_copy_BGR, cv2.COLOR_BGR2HSV)

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
                # 计算中间线
                center_line = get_center_line(l_border, r_border)

                # 创建一个彩色图像用于绘制边界
                result_image = cv2.cvtColor(largest_mask, cv2.COLOR_GRAY2BGR)

                for y in range(image_h):
                    if l_border[y] != border_min:
                    # 绘制左边界点，使用绿色
                        cv2.circle(result_image, (l_border[y], y), 1, (0, 255, 0), -1)

                    if r_border[y] != border_max:
                    # 绘制右边界点，使用红色
                        cv2.circle(result_image, (r_border[y], y), 1, (0, 0, 255), -1)
                
                    if center_line[y] is not None:
                        # 绘制中间线点，使用蓝色
                        cv2.circle(result_image, center_line[y], 1, (255, 0, 0), -1)

                    # 显示结果
                    cv2.imshow('Boundary Detection', result_image)
        


        # 按'q'键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

