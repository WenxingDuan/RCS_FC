import shutil

# 源文件路径
for i in range(26, 51,2):
    src_dir = "C:\\Users\Duan\OneDrive - University of Edinburgh\\Year 4\\毕设\\doi_10.5061_dryad.k6t1rj8__v11\\n" + str(
        i) + "_m14\\"

    # 目标文件路径
    dest_dir = "Full Circuit\\e0_" + str(i)+"\\"
    for j in range(0, 10):
        try:
            src_file = src_dir + "measurements_n"+str(i)+"_m14_s" + str(
                j) + "_e0_pEFGH.txt"
            dest_file = dest_dir + "measurements_n"+str(i)+"_m14_s" + str(
                j) + "_e0_pEFGH.txt"
        # 复制文件
            shutil.copy(src_file, dest_file)  # `copy()`函数只复制文件内容和权限位
        # shutil.copy2(src_file, dest_file)  # `copy2()`函数除了复制文件内容和权限位外，还会尽量保持文件的元数据(如修改时间等)
        except:
            src_file = src_dir + "measurements_n"+str(i)+"_m14_s1" + str(
                j) + "_e0_pEFGH.txt"
            dest_file = dest_dir + "measurements_n"+str(i)+"_m14_s" + str(
                j) + "_e0_pEFGH.txt"
        # 复制文件
            shutil.copy(src_file, dest_file)  # `copy()`函数只复制文件内容和权限位
        # shutil.copy2(src_file, dest_file)  # `copy2()`函数除了复制文件内容和权限位外，还会尽量保持文件的元数据(如修改时间等)
