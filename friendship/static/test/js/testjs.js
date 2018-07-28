                $(function() {
                $(".dropdown").hover(
                    function(){ $(this).addClass('open') },
                    function(){ $(this).removeClass('open') }
                );

//
// active_tab= $(document.body).attr('data-id');
//    if(active_tab=='sfr'){
//    $('#sent-requests').addClass('in active');
//    $('#sfr').addClass('active');
//       }
//       else if(active_tab=='f')
//       {
//        $('#friends').addClass('in active');
//    $('#f').addClass('active');
//       }
//       else if(active_tab=='op')
//       {
//        $('#other-people').addClass('in active');
//    $('#op').addClass('active');
//       }
//       else
//       {
//        $('#received-requests').addClass('in active');
//    $('#rr').addClass('active');
//    }

//
    //ajax for real time
setInterval(function () {
    $.ajax({
        url: "/friendship/test/",
        success: function (data) {
         $('#here').html(data)
   $('a[data-toggle="tab"]').on('click', function(e) {
        window.localStorage.setItem('activeTab', $(e.target).attr('href'));
    });

    var activeTab = window.localStorage.getItem('activeTab');
    if (activeTab) {
        $('#myTab a[href="' + activeTab + '"]').tab('show');
//        window.localStorage.removeItem("activeTab");
    }

        }
    });
}, 10000);
    //ajax

   $('a[data-toggle="tab"]').on('click', function(e) {
        window.localStorage.setItem('activeTab', $(e.target).attr('href'));
    });

    var activeTab = window.localStorage.getItem('activeTab');
    if (activeTab) {
        $('#myTab a[href="' + activeTab + '"]').tab('show');
//        window.localStorage.removeItem("activeTab");
    }

            });


