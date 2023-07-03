import cv2
import os

num = 0
def stitch():
    global num
    mainFolder = 'Image'
    myFolders = os.listdir(mainFolder)
    # 打印我们Image文件夹中所有文件和文件夹的名称
    print(myFolders)

    for folder in myFolders:
        path = mainFolder + '/' + folder
        images = []
        myList = os.listdir(path)
        # 打印图片
        print(myList)
        for imgN in myList:
            curImg = cv2.imread(f'{path}/{imgN}')
            #curImg = cv2.resize(curImg,(300,300))
            images.append(curImg)

        # 实例化拼接器
        stitcher = cv2.Stitcher.create()
        (status, result) = stitcher.stitch(images)
        #result = cv2.resize(result,(1800,600))
        # 如果拼接成功就显示成功
        if (status == cv2.STITCHER_OK):
            print("Panorama Generated")
            cv2.imwrite("./output/Panorama" + str(num) + ".jpg", result)
            num += 1
        else:
            print('Panorama Generation Unsuccessful')
