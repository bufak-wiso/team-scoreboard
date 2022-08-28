<?php

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
					'<div class="formLabel">Passwort <span id="labelPwdHome">Heimmanschaft</span></div>'.
					'<div id = "homePwd">'.
						'<input data-name="homePwd" class="formItem" type="text">'.
					'</div>'.
					'<div class="formLabel">Passwort <span id="labelPwdGuest">Gastmannschaft</span></div>'.
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
?>