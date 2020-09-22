<?php

function get_data($filename) {
	$contents = file_get_contents($filename);
	$data = json_decode($contents, true);
	shuffle($data['data']);
	if ($data['meta']['format'] == 'index' and !empty($data['data'])) {
		$item = array_rand($data['data']);
		$nextfile = dirname($filename) . '/' . $data['data'][$item];
		return get_data($nextfile);
	} else {
		$data['meta']['filename'] = $filename;
		$selected = array_rand($data['data'], 8);
		$data['data'] = array_intersect_key($data['data'], $selected);
		return $data;
	}
}

header('Content-type: application/json');
echo
	json_encode(
		#get_data('data/index.json'),
		get_data('data/language/indonesian/index.json'),
		JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
?>