<?php
function renderTable($apiUrl){
	$tableItems = "";
	$items = callApi($apiUrl."/get-scoreboard?category=1");
	for ($i = 0; $i<sizeof($items);$i++) {
		console_log($items[$i]);
		$count = $i+1;
		$tableItems .= '<div class = "tableItem">'.
							'<div>'.$count.'</div>'.
							'<div>'.$items[$i]["name"].'</div>'.
							'<div>'.$items[$i]["wins"].'/'.$items[$i]["matches"].'</div>'.
						'</div>';
	}
	$table = 	"<div id = 'table'>".
				"<div class = 'tableHeader'>".
					"<div>Platzierung</div>".
					"<div>Team</div>".
					"<div>Siege</div>".
					"</div>".
					$tableItems.
				"</div>";
	return $table;
}
?>