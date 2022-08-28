function postGameRestult (apiUrl){
    let match = {};
    let formValues = jQuery(".formItem");
    for (let i = 0; i<formValues.length;i++){
        let value = jQuery(formValues[i]).val();
        let key = jQuery(formValues[i]).attr("data-name");
        match[key] = value;
    };
    match.cId=1;
    if (!match.homeScore){
        if(match.winnerId == match.homeId){
            match.homeScore = 1;
            match.guestScore = 0;
        } else if(match.winnerId == match.guestId){
            match.homeScore = 0;
            match.guestScore = 1;
        }
    }
    console.log(match)
    let jsonString = JSON.stringify(match);
    jQuery.ajax({
        type: "POST",
        url: apiUrl,
        contentType: "application/json; charset=utf-8",
        data: jsonString,
        success : function(data){
            jQuery("#success").addClass("hidden");
            jQuery("#error").addClass("hidden");
            response = JSON.parse(data);
            if(response.success){
                jQuery("#success").removeClass("hidden");
                jQuery("#gameForm").addClass("hidden");
            } else {
                jQuery("#error .apiMessage").text(response.msg);
                jQuery("#error").removeClass("hidden");
            }
        },
        error : function(data){
            console.log(data)
        }
    });
}

function changeWinnerOptions (){
    let el = jQuery(".formItem[data-name='winnerId']");
    jQuery(el).empty(); // remove old options
    el.append(jQuery("<option></option>").attr("value", jQuery(".formItem[data-name='homeId']").val()).text(jQuery(".formItem[data-name='homeId'] option:selected").text()));
    el.append(jQuery("<option></option>").attr("value", jQuery(".formItem[data-name='guestId']").val()).text(jQuery(".formItem[data-name='guestId'] option:selected").text()));

    jQuery("#labelPwdHome").text(jQuery(".formItem[data-name='homeId'] option:selected").text());
    jQuery("#labelPwdGuest").text(jQuery(".formItem[data-name='guestId'] option:selected").text());
}