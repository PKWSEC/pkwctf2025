<?php
highlight_file('index.php');

#一句话木马，神神又奇奇

if(isset($_POST['J'])){
    $call=$_POST['J'];
    $dangerous_commands = ['cat', 'tac', 'head', 'nl', 'more', 'less', 'tail', 'vi', 'sed', 'od'];
    foreach ($dangerous_commands as $command) {
        if (preg_match("/$command/i", $call)) {
            die("这些个危险函数可不兴使啊");
        }
    }
    system($call);
}
?>