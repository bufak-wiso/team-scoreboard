<?php
/**
 * Plugin Name: teamscoreboard
 * Plugin URI: https://github.com/bufak-wiso/team-scoreboard
 * Description: BuFaK WiWi Scoreboard Plugin
 * Version: 0.1
 * Author: Moritz Bunse
 * Author URI: https://mobunse.de
 */

require( plugin_dir_path( __FILE__ ) . '/includes/gameForm.php');
require( plugin_dir_path( __FILE__ ) . '/includes/table.php');
require( plugin_dir_path( __FILE__ ) . '/includes/regForm.php');
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
	}elseif($atts["pagetype"]=="regform"){
		$content = renderRegForm($apiServerUrl,$gameYear);
	}

	return $content;
}

add_shortcode('teamscoreboard', 'teamscoreboard_plugin');

function callApi($url){
	return json_decode(file_get_contents($url),true);
}
function console_log( $data ){
	echo '<script>';
	echo 'console.log('. json_encode( $data ) .')';
	echo '</script>';
  }


?>