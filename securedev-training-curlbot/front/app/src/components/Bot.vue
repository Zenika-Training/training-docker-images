<template>
  <div class="container" v-if="bot">
    <div class="row">
    <div v-show="error" class="alert alert-danger" role="alert">
      {{ error }}
    </div>
    <div v-show="success" class="alert alert-success" role="alert">
      {{ success }}
    </div>
    <div class="alert alert-warning" role="alert" v-if="!success">
      Your bot is broken ? Send the link to the administrator by clicking on this button : <button class="btn btn-warning" v-on:click="sendLink"><b>Repair it please !</b></button>
    </div>
    </div>
    <div class="row">
      <div class="col-lg-3">
        <img :src="robotHashUrl(bot.name)">
      </div>
      <div class="col-lg-6" style="margin-left: 50px;">
        <b>ID</b>
        <p>{{ bot.id }}</p>
        <b>Name</b>
        <p>{{ bot.name }}</p>
        <b>Description</b>
        <p>{{ bot.description }}</p>
        <b>URL</b>
        <p>{{ bot.url }}</p>
        <b v-if="bot.credentials">Credentials</b>
        <p v-if="bot.credentials">{{ bot.credentials }}</p>
        <button class="btn btn-success" v-on:click="publicPage">Public page</button>
        <button class="btn btn-danger" v-on:click="deleteRobot" style="margin-left: 20px;">Delete</button>
      </div>  
    </div>       
  </div>   
</template>
<script>
import axios from 'axios'
export default {
    watch: {
      '$route.params.id': function () {
        this.loadRobot();
      }
    },
    data: function () {
      return {
        bot: undefined,
        name: undefined,
        pub_desc: undefined,
        priv_desc: undefined,
        error: undefined,
        success: undefined
      }
    },
    methods: {
      sendLink: function(){
        var that = this;
        axios.get("/api/v1/broken",{
            params: {link: that.getPublicLink()},
        },
        {withCredentials: true}).then(
          response => {
              that.error = undefined;
              if(response.data.status=="error"){
                  that.error = response.data.message;
              }
              else if(response.data.status=="success"){
                that.success = response.data.message;
              }
          })
      },
      robotHashUrl: function (name) {
        return "https://robohash.org/"+name
      },
      getPublicLink: function(){
        var link = btoa(JSON.stringify(this.bot));
        return "/public/"+link.replace(/\+/g, '-').replace(/\//g, '_')
      },
      publicPage: function(){
        window.location.href = this.getPublicLink()
      },
      loadRobot: function(){
        var that = this;
        axios.get("/api/v1/robot/"+this.$route.params.id,{withCredentials: true})
        .then(
        response => {
          if(response.data.status=="error"){
            that.$router.push('/bots', () => {})
          }
          else{
            that.bot = response.data;
          }
        })
      },
      deleteRobot: function(){
        var that=this;
        axios.delete("/api/v1/robot/"+this.$route.params.id,{withCredentials: true})
        .then(function() {
            that.$router.push('/bots', () => {})
        })
      }
    },
    mounted() {
      this.loadRobot();
    },
}
</script>