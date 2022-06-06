const Index = {
    delimiters:['${','}'],
    data(){
        return {
            id: '',
            title: '',
            tags: [],
            date: '2022/06/12',
            content: '<h4>Flask + vue</h4>'
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
            })
            .then(function (response) {
            console.log(response);
            })
            .catch(function (error) {
            console.log(error);
            });
        },
        get_blog: function(){
            let vm = this
            axios.get('/post/get_post/',{
                params: {
                post_id: vm.id
                }
              }).then(function (response) {
                vm.title = response.data.title;
                vm.tags = response.data.tags;
                vm.date = response.data.date;
                vm.content = response.data.content;
              })
        }
    }
}

blog = Vue.createApp(Index).mount('#main')
blog.id = document.getElementById("post_id").getAttribute('name')
if(blog.id!=''){
    blog.get_blog()
}
