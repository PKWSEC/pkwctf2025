<?php

// 设置文件包含的根目录
$base_dir = 'uploads/';
if(isset($_GET['file'])){
    $file = $_GET['file'];
    include($file);
}
?>