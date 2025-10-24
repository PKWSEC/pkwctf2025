<?php
namespace app\index\controller;

class Index {
	public function index() {
		$res = "<style>a{font-size:50px}</style><h1>Thinkphp框架</h1>";
		$http_type = ((isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] == 'on') || (isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && $_SERVER['HTTP_X_FORWARDED_PROTO'] == 'https')) ? 'https://' : 'http://';
		return $res;
	}
}
