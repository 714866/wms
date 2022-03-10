$(function(){

    yeshu(0)
function yeshu(foc){
		total_pages=$('.common_title2').attr('id')/2
        if ((total_pages-foc)>-1){
            if(foc==0){
                if(total_pages<=10){
                    for(i=1; i<=total_pages;i++){
                        $('#next').before('<a href="#" class="" id="list'+i+'">'+i+'</a>');
                    }
                }else{
                    for(i=1; i<=10;i++){
                        $('#next').before('<a href="#" class="" id="list'+i+'">'+i+'</a>');
                    }
                    $('#next').before('<a href="#" class="" id="xlist">...</a>');
                }
                $('#list1').attr('class','active');
            }

            else if(total_pages<=10){
                $('.pagenation a').attr('class','');
                $('#list'+foc).attr('class','active');
            }else{
                console.log('....')
                if(foc<=5){
                console.log('小于5')
                    for(i=1;i<=10;i++){
                        $('#list'+i+'').text(i)
                    }
                $('.pagenation a').attr('class','');
                $('#list'+foc+'').attr('class','active');
                $('#xlist').show()
                }else{

                    if(total_pages-foc<5){
                        for(i=0;i<=(total_pages-foc);i++){
                            m=10-i
                            $('#list'+m+'').text(total_pages-i);
                        }
                        for(i=1;i<=10-(total_pages-foc);i++){
                            d=total_pages-10+i
                            $('#list'+i+'').text(d);

                        }

                        $('.pagenation a').attr('class','');
                        d=10-total_pages+foc
                        $('#list'+d+'').attr('class','active')
                        $('#xlist').hide();

                    }else{
                        console.log('大于5')
                        for(i=0;i<5;i++){
                            m=6+i
                            $('#list'+m+'').text(foc+i);
                            n=5-i
                            $('#list'+n+'').text(foc-i-1);

                        }
                        $('.pagenation a').attr('class','');
                        $('#list6').attr('class','active');
                        $('#xlist').show();
                    }

                }




		    }
        }else{

        }

}
function huanye(number){



		$.get('/user/user_order_headle/?index='+number,function(data){
		    if (data.status==0){
                console.log(data.status)
		    }else
		    {
                var k = 0
                console.log(data.goods)
                $('.order_list_th').empty();
    //            $('.order_list_th').remove();  使用remove使得表单都不见了
                $('.order_goods_list').empty();
                $.each(data.goods,function(index,itm){
                    console.log(itm.g_l[0].gprice)
                    var context ='<li class="col01">'+itm.odate+'</li>'
                                    +'<li class="col02">订单号：'+itm.oid+'</li>'
                                    +'<li class="col02 stress" status='+itm.ostatus+'>未支付</li>'


                    $('.order_list_th').eq(index).prepend(context);
                    console.log(itm.g_l)
                    $.each(itm.g_l,function(gindex,item){
                    console.log('是否成功')
                        var context2='<ul class="order_goods_list clearfix">'
                                        +'<li class="col01"><img src="/static/'+item.gpic+'"></li>'
                                        +'<li class="col02">'+item.gtitle+'<em>'+item.gprice+'元/'+item.gunit+'</em></li>'
                                        +'<li class="col03">'+item.count+'</li>'
                                        +'<li class="col04">'+item.gprice+'元</li>'
                                        +'</ul>'
                        console.log(index,gindex)

                        $('.order_list_table ').eq(index).find('td').first().prepend(context2);

                    });

                    $('.order_list_table').eq(index).find('td').eq(1).text(itm.ototal);
                    if(itm.ostatus==0){
                        $('.order_list_table').eq(index).find('td').eq(2).text('待付款');
                    }else{
                        $('.order_list_table').eq(index).find('td').eq(2).text('已付款');
                        $('.order_list_table').eq(index).find('td').eq(3).text('待发货');
                    }
                    k=index
                });
                if(k < 6){
                    for(i=k+1;i<=10;i++){
                        $('.order_list_th').eq(k+1).remove();
                        $('.order_list_table').eq(k+1).remove();
                        }
                }
            }
		});


}




	$("a[id^='list']").click(function(){               <!-- 分页用的    -->
		$('.pagenation a').attr('class','');
		$(this).attr('class','active');

		var number=parseInt($(this).text())
		yeshu(number)
		huanye(number)
	});

	$("a[id^='next']").click(function(){
		var number
		var number=parseInt($('.pagenation a[class=active]').text())+1   <!-- 下一页 获取到页数了-->
		yeshu(number)
		huanye(number)
		console.log(3/2)
	});

	$("a[id^='super']").click(function(){
		var number
		var number=parseInt($('.pagenation a[class=active]').text())-1   <!-- 下一页 获取到页数了-->
		if(number>0){
			yeshu(number)
			huanye(number)

		}
	});



})