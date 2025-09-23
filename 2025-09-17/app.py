import os


file_types = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".doc", ".docx", ".txt"],
    "Music": [".mp3", ".wav"],
    "Others": []
}

root_path = ".\Downloads"


# 檢查資料夾是否存在
for folder_name in file_types.keys():
    folder_path = os.path.join(root_path, folder_name)
    if not os.path.exists(folder_path):
        print(f"{folder_name} 資料夾不存在")
        os.makedirs(folder_path)
        print(f"{folder_name} 資料夾已建立")
    else:
        print(f"{folder_name} 資料夾已存在")


# 獲取root_path內所有檔案及資料夾，並且按照file_types分類然後移動檔案
for files in os.listdir(root_path):
    file_path = os.path.join(root_path, files)  
    if os.path.isfile(file_path):
        print(files + "是檔案")
        file_ext = os.path.splitext(files)[1].lower()
        
        for category, extensions in file_types.items():
            if file_ext in extensions:
                os.rename(file_path, os.path.join(root_path, category, files))
                print(f"已將 {files} 移動到 {category} 資料夾")
                break
        
        # 判斷檔案是否已經搬移
        if not os.path.exists(file_path):
            # print(f"已將 {files} 搬移")
            continue

        os.rename(file_path, os.path.join(root_path, "Others", files))
        print(f"已將 {files} 移動到 Others 資料夾")
           
    else:
        print(files + "不是檔案")
