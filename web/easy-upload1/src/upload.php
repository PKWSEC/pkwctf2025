<?php
// 上传目录
$uploadDir = 'upload/';

// 确保上传目录存在
if (!file_exists($uploadDir)) {
    mkdir($uploadDir, 0777, true);
}

// 检查是否有文件上传
if (isset($_FILES['file'])) {
    $file = $_FILES['file'];
    $fileName = $file['name'];
    $fileTmpName = $file['tmp_name'];
    $fileSize = $file['size'];
    $fileError = $file['error'];
    
    // 检查上传错误
    if ($fileError === UPLOAD_ERR_OK) {
        // 移动文件到上传目录，保持原始文件名
        $destination = $uploadDir . $fileName;
        
        if (move_uploaded_file($fileTmpName, $destination)) {
            // 返回文件路径
            echo $destination;
        } else {
            echo "文件移动失败";
        }
    } else {
        echo "上传错误: " . $fileError;
    }
} else {
    echo "没有文件被上传";
}
?>