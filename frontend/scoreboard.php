<?php
/*
Plugin Name: Team Scoreboard Frontend
Description: 
Version: 1.0
Author: Moritz Bunse 
Author URI: https://github.com/bufak-wiso/team-scoreboard/
*/
defined( 'ABSPATH' ) or die( 'Are you ok?' );

$start_reminder = new UpdateReminder();

class UpdateReminder{

	public function __construct() {

		register_activation_hook( __FILE__, array( $this, 'updateReminder_activate' ) );
		
		register_deactivation_hook(__FILE__, array( $this, 'updateReminder_deactivation' ) );
		
		add_action( 'updateReminderEvent', array( $this, 'getUpdateStatus' ) );
	}

	public function getUpdateStatus(){

		$status = wp_get_update_data();

		if ( $status['counts']['total'] != 0 ) {
			
			$mail = get_option( 'admin_email' );
			$blogname = get_option( 'blogname' );
			
			if ( $mail ) {
				wp_mail(
					$mail,
					'Update Benachrichtigung ' . $blogname,
					'Für deinen Blog "' . $blogname . '" stehen ' . $status['counts']['total'] . ' Updates zur Verfügung.<br>
					' . $status['counts']['plugins'] . ' Plugin Updates<br>
					' . $status['counts']['themes'] . ' Theme Updates</br>
					' . $status['counts']['wordpress'] . ' WordPress Core Updates<br>
					' . $status['counts']['translations'] . ' Übersetzungs Updates',
					'Content-Type: text/html; charset=UTF-8'
				);
			}
		}
	}

	public function updateReminder_activate(){
		if (! wp_next_scheduled ( 'updateReminderEvent' )) {
			wp_schedule_event( time(), 'daily', 'updateReminderEvent' );
		}
	}

	public function updateReminder_deactivation(){
		if ( wp_next_scheduled( 'updateReminderEvent' ) ) {
			wp_clear_scheduled_hook( 'updateReminderEvent' );
		}
	}

}