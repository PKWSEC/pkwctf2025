<?php
header('Content-Type: text/plain; charset=utf-8');

// 定义允许上传的扩展名
$allowed_exts = array('jpg', 'jpeg', 'png', 'gif');
$upload_dir = 'uploads/';

// 创建上传目录（如果不存在）
if (!file_exists($upload_dir)) {
    mkdir($upload_dir, 0755, true);
}

// 检查文件上传是否成功
if ($_FILES['file']['error'] !== UPLOAD_ERR_OK) {
    die('文件上传失败，错误代码: ' . $_FILES['file']['error']);
}

// 获取文件信息
$file_name = $_FILES['file']['name'];
$file_tmp = $_FILES['file']['tmp_name'];
$file_size = $_FILES['file']['size'];
$file_ext = strtolower(pathinfo($file_name, PATHINFO_EXTENSION));

// 安全检查：扩展名白名单
if (!in_array($file_ext, $allowed_exts)) {
    die('错误：只允许上传 JPG, JPEG, PNG 或 GIF 文件。');
}

// 安全检查：文件类型
$finfo = finfo_open(FILEINFO_MIME_TYPE);
$mime = finfo_file($finfo, $file_tmp);
finfo_close($finfo);

$allowed_mimes = array(
    'jpg' => 'image/jpeg',
    'jpeg' => 'image/jpeg',
    'png' => 'image/png',
    'gif' => 'image/gif'
);

if (!in_array($mime, $allowed_mimes)) {
    die('错误：文件类型不符合要求。');
}

// 安全检查：文件内容（防止图片马）
if (!getimagesize($file_tmp)) {
    die('错误：上传的文件不是有效的图片。');
}

// 生成安全的文件名
$new_file_name = uniqid() . '.' . $file_ext;
$destination = $upload_dir . $new_file_name;

// 移动文件到上传目录
if (move_uploaded_file($file_tmp, $destination)) {
    echo '文件上传成功！路径: ' . $destination;
} else {
    echo '错误：文件保存失败。';
}
?>