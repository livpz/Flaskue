const Index = {
    delimiters:['${','}'],
    data(){
        return {
            click_count: 0,
            pagesum: 1,
            index: 1,
            pagelist: [],
            start: 1,
            end:1,
            logout_click: 0,
            hot_base: "/index/static/img/hot_base.png",
            static_root: "/index/static/BluePrint/index_bp/static/",
            title_list: []
        }
    },
    methods: {
        open_blogpage: function(event){
            console.log(event.target)
            let id_ = event.target.getAttribute('value')
            window.location.href=  "/post/page?post_id=" + id_
        },
        get_blog_list: function(e){
            let vm = this;
            if(e){
                pageindex = e.target.getAttribute('page')
                if(vm.index == pageindex){
                    return 0
                }
                vm.index = pageindex
            }

            axios.get('/post/get_post_list/',{
                params: {
                index: vm.index
                }
            }).then(function (response) {
                console.log(response);
                vm.title_list = response.data.post_list;
                vm.pagesum = response.data.page_sum;
                vm.set_pagelist()
            })
        }, set_pagelist: function(){
            let vm = this
            vm.pagelist = []
            var page = vm.index
            let pageindex = parseInt(page)

            for(i of [-1,-2,-3]){
                i = parseInt(i)
                pageitem = pageindex + i
                if( pageitem > 1){
                    console.log('pageitem:',pageitem)
                    vm.pagelist.push(pageitem)
                }
            }
            for(i of [1,2,3]){
                i = parseInt(i)
                pageitem = pageindex + i
                if( pageitem < vm.pagesum){
                    console.log('pageitem:',pageitem)
                    vm.pagelist.push(pageitem)
                }
            }
            if(page!=1 && page != vm.pagesum){
                console.log('pageitem:',pageitem)
                vm.pagelist.push(page)
            }
            vm.pagelist.sort((a, b) => a - b)
            vm.start = vm.pagelist[0]
            vm.end = vm.pagelist[vm.pagelist.length - 1]
        },
        count_to_write: function(){
            let vm = this;
            vm.click_count += 1
            if(vm.click_count==3){
                vm.click_count = 0
                window.location.href = '/post/write/'
            }
        },
        logout: function(){
            let vm = this
            vm.logout_click += 1
            console.log(vm.logout_click)
            if(vm.logout_click >= 4){
            window.location.href = '/index/logout/'
            }
        }
    }
}

var index = Vue.createApp(Index).mount('#main')
index.get_blog_list()
