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
    // Global: pie
    authors_info = data.commits_global.slice (0,10);
    console.log (authors_info);
    Flotr.draw (document.getElementById("global_graph_pie"), authors_info, {
	   HtmlText : false,
	   pie : {
		  show : true,
		  explode : 9,
	   },
	   grid : {
		  verticalLines : false,
		  horizontalLines : false
	   },
	   mouse : {
		  track : true,
        },
	   legend : {
		  position : 'se',
		  backgroundColor : '#D2E8FF'
	   },
	   xaxis : { showLabels : false },
	   yaxis : { showLabels : false },
    });

    // Developer: stacked
    authors_info = data.commits_num.info.slice (0,10);
    Flotr.draw (document.getElementById("graph_time"), authors_info, {
	   bars: {
		  show: true,
		  stacked : true,
	   },
        mouse : {
		  track : true,
		  relative : true
        },
	   legend: {
		  noColumns: 5,
		  container: $("#global_legend")
	   },
	   xaxis : {
		  tickFormatter: function (num) {
			 unixtime = data.time_start + (num * data.time_lapse);
			 date = new Date (unixtime * 1000);
			 return MONTH_NAMES[date.getMonth()] + date.getYear()%100;
		  }
	   },
	   yaxis : {
		  // min: 0,
		  // max: data.commits_num.highest_value + (data.commits_num.highest_value * 0.10),
		  autoscaleMargin : 1,
		  tickDecimals: 0,
	   }
    });
}

function get_author_LI (author)
{
    var txt = author.label + ' (' + author.total + ')';
    if (author.companies[0]) {
	   txt += '<span class="author_company">'+ author.companies[0] + '</span>';
    }
    return '<li>'+ txt +'</li>';
}

function populateAuthorsList (data)
{
    authors_info = data.commits_num.info;

    for (n in data.commits_num.info) {
	   if (authors_info[n].total == 0)
		  break;

	   $((n < 10)? "#contributors_top10":"#contributors").append (get_author_LI(authors_info[n]));
    }
}


$(function() {
    var project = getURLParameter("project").replace(/[^a-z-]+/gi,'');
    var release = getURLParameter("release").replace(/[^a-z-]+/gi,'');

    if (!project || !release)
	   return;

    $("h1").html(capitalise(project))
    $("h3").html(capitalise(release) + ' release');

    $.ajax({
	   url:      'json/authors-' + project+'-'+release+'.js',
	   dataType: 'json',
	   error:     function (e) {console.log(e);},
	   success:   function (data)
	   {
		  addGlobalReport (data);
		  populateAuthorsList (data);
	   }
    });
});
