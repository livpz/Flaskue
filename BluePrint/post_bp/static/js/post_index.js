const Index = {
    delimiters:['${','}'],
    data(){
        return {
            title: 'Post 文章标题.',
            tags: ['tag1','tag2'],
            date: '2022/06/12',
            view_count: '1234',
            content: '<h4>Flask + vue</h4>',
            body_click: 0,
            head_click: 0
        }
    },
    methods: {
        get_blog: function(){
            let vm = this
            id_ = document.getElementById("post_id").getAttribute('name')
            axios.get('/post/get_post/',{
                params: {
                post_id: id_
                }
              }).then(function (response) {
                console.log(response);
                vm.title = response.data.title;
                vm.tags = response.data.tags;
                vm.date = response.data.date;
                vm.content = response.data.content;
                vm.view_count = response.data.view_count;
              })
        },
        edit: function(){
            id_ = document.getElementById("post_id").getAttribute("name")
            window.location.href='/post/write?post_id=' + id_
        },
        click_body: function(){
            let vm = this
            vm.body_click += 1
            if(vm.body_click > 5){
                vm.head_click=0
                vm.body_click=0
            }
        },
        click_head: function(){
            let vm = this
            vm.head_click += 1
            if(vm.head_click==2 && vm.body_click==2){
                vm.edit()
            }
        }
    }
}

blog = Vue.createApp(Index).mount('#main')
blog.get_blog()
