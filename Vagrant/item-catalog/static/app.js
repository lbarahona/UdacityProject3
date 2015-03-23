/**
 * This document has various JS/jQuery based functions for use in the
 * single page catalog application
 */

/**
 * this function is for the accordian menu function and display
 */
$(function() {
    $(".accmentitle").click(function() {
        if (event.target.nodeName == "DIV"){
            $(this).find(".fa:first").toggleClass( 'fa-chevron-down fa-chevron-up' );
            var ul = $(this).next(),
                height = ul.css("height") === "0px" ? ul[0].scrollHeight + "px" : "0px";
            
            ul.animate({"height":height});
            return false;
        }
    });
});

/**
 * This is a jQuery based hover over tooltip function.  Anything with the class
 * tooltip will get a hover over tip based on it's data-tip.  Anything starting
 * with an ! will be given a class of danger for it's text as well.
 */
$(function() {
    var tipElement = $('<div class="dyntooltip"></div>')
    .appendTo('body')
    .fadeIn('slow')
    .css({ top: -10000, left: -10000  });

    $('.tip').hover(function(){
            // Hover over code
            var curTitle = $(this).data('tip');
            if (curTitle.charAt(0) === "!") {
                curTitle = '<span class="danger">' + curTitle.slice(1) + '</span>';
            }
            if (curTitle) {
                tipElement.html(curTitle);
            }
    }, function(e) {
            tipElement.html('');
            tipElement.css({ top: -10000, left: -10000  });
    }).mousemove(function(e) {
            var mousex = e.pageX - tipElement.width()/1.8; //Get X coordinates
            var mousey = e.pageY - tipElement.height()*3; //Get Y coordinates
            tipElement.css({ top: mousey, left: mousex });
    });
});

/**
 * AJAX request for reset all data confirmation to use in the shared modal
 * this should not be left in production environments without additional checks
 * @param  int company_id Company id in our database for the company to delete from
 * @param  int item_id    SalesItem id in our database for the item to delete
 */
var openResetData = function() {
  $.getJSON('/resetdatajson', openModal);
  return false;
};

/**
 * AJAX request for company delete confirmation to use in the shared modal
 * @param  int company_id Company id in our database for the company to delete from
 * @param  int item_id    SalesItem id in our database for the item to delete
 */
var openDeleteItem = function(company_id,item_id) {
  $.getJSON('/deleteitemjson', {
    company_id: company_id,
    item_id: item_id
  }, openModal
  );
  return false;
};

/**
 * AJAX request for company add for use in the shared modal
 */
var openCompanyAdd = function() {
  $.getJSON('/addcompanyjson', openModal );
  return false;
};

/**
 * AJAX request for company add for use in the shared modal
 * @param  int company_id Company id in our database that the item will be added to
 */
var openItemAdd = function(company_id) {
  $.getJSON('/additemjson', {
    company_id: company_id
  }, openModal
  );
  return false;
};

/**
 * AJAX request for item edit form to use in the shared modal
 * @param  int company_id Company id in our database (the company of this item)
 * @param  int item_id    SalesItem id in our database (item to edit)
 */
var openEditItem = function(company_id,item_id) {
  $.getJSON('/edititemjson', {
    company_id: company_id,
    item_id: item_id
  }, openModal
  );
  return false;
};

/**
 * AJAX request for item edit form to use in the shared modal
 * @param  int companyId Company id in our database (the company of this item)
 * @param  int itemId    SalesItem id in our database (item to edit)
 */
var openEditCompany = function(company_id) {
  $.getJSON('/editcompanyjson', {
    company_id: company_id
  }, openModal
  );
  return false;
};

/**
 * AJAX request for company delete confirmation to use in the shared modal
 * @param  int company_id Company id in our database for the company to delete
 */
var openDeleteCompany = function(company_id) {
  $.getJSON('/deletecompanyjson', {
    company_id: company_id
  }, openModal
  );
  return false;
};

/**
 * AJAX request for item information to use in the shared modal
 * @param  int company_id Company id in our database
 * @param  int item_id    SalesItem id in our database
 */
var openItem = function(company_id,item_id){
  $.getJSON('/itemjson', {
    company_id: company_id,
    item_id: item_id
  }, openModal
  );
  return false;
};

/**
 * Shared function for use opening the modal after a JSON ajax query returns
 * @param  AJAX reply response This is the AJAX reply
 */
openModal = function(response) {
   $("#itemModal").html(response.result);
   
   $.magnificPopup.open({
      items: {
          type: 'inline',
          src: $("#itemModal")
      }
   });
};

/**
 * Closes the shared modal if it is open
 */
var closeModal = function(){
    $.magnificPopup.close();
};