<?php
/**
 * Plugin Name: teamscoreboard
 * Plugin URI: https://github.com/bufak-wiso/team-scoreboard
 * Description: BuFaK WiWi Scoreboard Plugin
 * Version: 0.1
 * Author: Moritz Bunse
 * Author URI: https://mobunse.de
 */


 function teamscoreboard_plugin($atts) {
		require( plugin_dir_path( __FILE__ ) . 'config.php');

		
		// load js
		wp_enqueue_script( 'catalog_functions', plugins_url( '/js/scoreboard.js', __FILE__ ));
    
		//load css
		wp_register_style('scoreboard_style', plugins_url('/css/scoreboard.css',__FILE__ ), $ver="1.0");
		wp_enqueue_style('scoreboard_style');
	if($atts["pagetype"]=="form"){
		$content = renderGameForm($apiServerUrl);
	}elseif($atts["pagetype"]=="table"){
		$content = renderTable($apiServerUrl);
	}

	return $content;
}

add_shortcode('teamscoreboard', 'teamscoreboard_plugin');


function renderGameForm ($apiUrl){
	$teamList = callApi($apiUrl."/get-teams");
	$optionsHtml = "";
	for ($i = 0;$i<sizeof($teamList["teams"]);$i++){
		$team=$teamList["teams"][$i];
		$optionsHtml.="<option value='".$team["tId"]."'>".$team["name"]."</option>";

	}
	$postUrl = "'".$apiUrl."/add-match'";
	$gameForm = '<div id="success" class="hidden">Das Ergebnis wurder erfolgreich eingetragen!</div>'.
				'<div id="error" class="hidden">Beim übertragen der Daten ist folgender Fehler aufgetreten:<br><span class="apiMessage">Lorem Ipsum Test Error</span></div>'.
			 	'<div id = "gameForm">' .
					'<div class="formLabel">Heimmanschaft</div>'.
					'<select data-name="homeId" onchange="changeWinnerOptions()" class="formItem">'.
						$optionsHtml.
					'</select>'.
					'<div class="formLabel">Gastmannschaft</div>'.
					'<select data-name="guestId" onchange="changeWinnerOptions()" class="formItem">'.
						$optionsHtml.
					'</select>'.
					'<div class="formLabel">Gewinner</div>'.
					'<select data-name="winnerId" class="formItem">'.
						$optionsHtml.
					'</select>'.
					'<div class="formLabel">Passwort <span id="labelPwdHome"></span></div>'.
					'<div id = "homePwd">'.
						'<input data-name="homePwd" class="formItem" type="text">'.
					'</div>'.
					'<div class="formLabel">Passwort <span id="labelPwdGuest"></span></div>'.
					'<div id = "guestPwd">'.
						'<input data-name="guestPwd" class="formItem" type="text">'.
					'</div>'.
					'<div>'.
						'<span id="submitBtn" onclick="postGameRestult('.$postUrl.')">Ergebnis eintragen</span>'.
					'</div>'.
				'</div>';
	//TODO: Frontend Check Felder

	return $gameForm;
}

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

function callApi($url){
	return json_decode(file_get_contents($url),true);
}
function console_log( $data ){
	echo '<script>';
	echo 'console.log('. json_encode( $data ) .')';
	echo '</script>';
  }


?>