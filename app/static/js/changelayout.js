

$("#navbar-changelayout" ).click(
    function(event){
        $.each(mydf, function(author,series){
            $.each(series,function(item,books){
                console.log(item)
                console.log(books)
            }
            )

        }
        
        
        )


        // _xd = $('#book-accordion').load("/",{ limit: 25 });
        // console.log(mydf)
        console.log("Changing Layout")
    }
)
/**
 * [
 *  {series_name:[{title:x,series_position:y,object_key:z}]
 * 
 *  },
 *  {
 *  }
 * ]
 * 
 */