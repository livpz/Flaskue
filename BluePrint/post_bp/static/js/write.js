const Index = {
    delimiters:['${','}'],
    data(){
        return {
            id: '',
            title: '',
            tags: [],
            date: '2022/06/12',
            content: '<h4>Flask + vue</h4>',
            md_content: '',
            show: true,
            contentActive: 'block',
            mdActive: 'none'
        }
    },
    methods: {
        upload: function(){
            let vm = this
            axios.post('/post/upload/', {
                id: document.getElementById("post_id").getAttribute("name"),
                title : vm.title,
                tags : vm.tags,
                date : vm.date,
                content : vm.content,
                show: vm.show
            })
            .then(function (response) {
            console.log(response);
            window.location.href= '/index/'
            })
            .catch(function (error) {
            console.log(error);
            });
        },
        get_blog: function(){
            let vm = this
            axios.get('/post/get_post/',{
                params: {
                post_id: vm.id,
                edit:1
                }
              }).then(function (response) {
                vm.title = response.data.title;
                vm.tags = response.data.tags;
                vm.date = response.data.date;
                vm.content = response.data.content;
              })
        },
        change_show: function(){
            let vm = this
            vm.show = !vm.show
        },
        toMD: function(){
            let vm = this
            axios.post('/post/tomd/', {
                content: vm.content,
            })
            .then(function (response) {
            console.log(response);
            vm.md_content = response.data.md_content
            vm.contentActive = 'none'
            vm.mdActive = 'block'
            })
            .catch(function (error) {
            console.log(error);
            });
        },
        toRaw: function(){
            let vm = this
            vm.contentActive = 'block'
            vm.mdActive = 'none'
        }
    }
}

blog = Vue.createApp(Index).mount('#main')
blog.id = document.getElementById("post_id").getAttribute('name')
if(blog.id!=''){
    blog.get_blog()
}
