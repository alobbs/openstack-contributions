MONTH_NAMES = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

function getURLParameter (name)
{
    return decodeURI(
        (RegExp(name + '=' + '(.+?)(&|$)').exec(location.search)||[,null])[1]
    );
}

function capitalise (string)
{
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function addGlobalReport (data)
{
    /* List of 'checked' companies */
    var companies_activated = $("#companies").find("label").has("input:checkbox:checked").map(function(){
	   return $(this).attr('id').replace('control_graph_','');
    });

    /* Filter the data array */
    var companies_info = data.commits_num.info.filter (function(co){
	   var co_name = co.label.replace(/[^a-z]+/gi,'');
	   return $.inArray (co_name, companies_activated) >= 0;
    });

    /* Fix the names of the legend */
    // FIX ME: Something is broken here (Eg: Check and uncheck company)
    //   $.each (companies_info, function (n, obj) {
    //      obj.label = capitalise (obj.label);
    //   });

    /* Draw graph */
    Flotr.draw (document.getElementById("global_graph"), companies_info, {
	   legend: {
		  noColumns: 10,
		  container: $("#global_legend")
	   },
	   xaxis : {
		  tickFormatter: function (num) {
			 date = new Date(num * 1000);
			 return MONTH_NAMES[date.getMonth()] + date.getYear()%100;
		  }
	   },
	   yaxis : {
		  min: 0,
		  max: data.commits_num.highest_value,
		  tickDecimals: 0,
	   }
    });
}

function addCompanyReports (data)
{
    for (cn in data.commits_num.info) {
	   commits_num  = data.commits_num;
	   commits_size = data.commits_size;

	   company_data_num  = commits_num.info[cn];
	   company_data_size = commits_size.info[cn];

	   /* Company List */
	   if (company_data_num.total <=0) {
		  $("#lazy_fellows").append('<li>'+ capitalise(company_data_num.label) +'</li>');
		  continue;
	   }

	   /* Graphs placeholders */
	   id_graph      = "graph_"+company_data_num.label.replace(/[^a-z]+/gi,'');
	   id_graph_num  = id_graph + "_num";
	   id_graph_size = id_graph + "_size";

	   $('#graphs').append ("<div id='"+id_graph+"'>" +
					      "<div id='"+id_graph_num+"'></div>" +
					      "<div id='"+id_graph_size+"'></div>" +
					    "</div>");

	   $('#'+id_graph_num).css ('width',  '800px');
	   $('#'+id_graph_num).css ('height', '150px');
	   $('#'+id_graph_size).css('width',  '800px');
	   $('#'+id_graph_size).css('height', '145px');

	   /* Graph: number */
	   Flotr.draw (document.getElementById(id_graph_num), company_data_num,
				{title: company_data_num.label,
				 bars: {
					show: true,
					barWidth: 0.8,
					lineWidth: 10,
				 },
				 xaxis : { showLabels: false },
				 yaxis : {
					min: 0,
					max: commits_num.highest_value,
					tickDecimals: 0,
				 },
				 grid : {
					verticalLines : false,
					horizontalLines : true,
				 },
				 legend : {
					position : 'ne',
					noColumns: 3,
					margin: 300,
				 }
				});

	   /* Graph: Size */
	   Flotr.draw (document.getElementById(id_graph_size), company_data_size,
				{bars: {
				    show: true,
				    barWidth: 0.8,
				    lineWidth: 10,
				 },
				 xaxis : {
				 	tickFormatter: function (num) {
				 	    date = new Date(num * 1000);
					    return MONTH_NAMES[date.getMonth()];
				 	}
				 },
				 yaxis : {
				 	tickFormatter: function (num) {
					    return Math.round(num / 1024) + "Kb";
				 	},
					min: 0,
					max: commits_size.highest_value,
					tickDecimals: 0,
				 },
				 grid : {
					verticalLines : false,
					horizontalLines : true,
				 },
				 legend : {
					position : 'ne',
					noColumns: 3,
					margin: 300,
				 }
				});

	   /* Contributors lists */
	   var caption    = capitalise(company_data_num.label) +' ('+ company_data_num.total +')';
	   var control_id = "control_" + id_graph;
	   var len        = $("#contributors_top5").find("li").length;

	   if (len < 5) {
		  $('#contributors_top5').append('<li><label id="'+control_id+'"><input type="checkbox" checked/>'+caption+'</label></li>');
	   } else {
		  $('#contributors').append('<li><label id="'+control_id+'"><input type="checkbox"/>'+caption+'</label></li>');
		  $('#'+id_graph).hide()
	   }

	   $('#' + control_id).change (function() {
		  var checked  = $(this).find('input').is(':checked');
		  var graph_id = $(this).attr('id').replace('control_','');

		  if (checked) {
			 $('#'+graph_id).show();
		  } else {
			 $('#'+graph_id).hide();
		  }

		  addGlobalReport (data);
	   });
    }
}


$(function() {
    var project = getURLParameter("project").replace(/[^a-z]+/gi,'');
    var release = getURLParameter("release").replace(/[^a-z]+/gi,'');

    if (!project || !release)
	   return;

    $("h1").html(capitalise(release) +' : '+ capitalise(project));

    $.ajax({
	   url:       project+'-'+release+'.js',
	   dataType: 'json',
	   error:     function (e) {console.log(e);},
	   success:   function (data)
	   {
		  addCompanyReports (data);
		  addGlobalReport (data);
	   }
    });
});
