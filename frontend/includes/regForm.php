<?php
function renderRegForm ($apiUrl,$gameYear){
	$postUrl = "'".$apiUrl."/add-team'";
	$regForm = '<div id="success" class="hidden">Euer Team wurde erfolgreich eingetragen. Viel Erfolg!</div>'.
				'<div id="error" class="hidden">Beim eintragen eures Teams ist folgender Fehler aufgetreten:<br><span class="apiMessage">Lorem Ipsum Test Error</span></div>'.
			 	'<div id = "gameForm">' .
					'<div class="formLabel">Name</div>'.
                    '<div>'.
                        '<input data-name="name" class="formItem" type="text">'.
                    '</div>'.
					'<div class="formLabel">Teamspruch</div>'.
                    '<div>'.
                        '<input data-name="description" class="formItem" type="text">'.
                    '</div>'.
					'<div class="formLabel">Team Passwort</div>'.
                    '<div>'.
                        '<input data-name="pwd" class="formItem" type="text">'.
                    '</div>'.
						'<span id="submitBtn" onclick="addTeamToTournament('.$postUrl.','.$gameYear.')">Team eintragen</span>'.
					'</div>'.
				'</div>';
	//TODO: Frontend Check Felder

	return $regForm;
}
?>