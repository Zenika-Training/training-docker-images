<template>
  <div class="container">
    <h3>Create new Robot</h3>
    <div v-show="error" class="alert alert-danger" role="alert">
      {{ error }}
    </div>
    <div v-show="success" class="alert alert-success" role="alert">
      {{ success }}
    </div>
    <div class="row">
      <div class="col-lg-6">
        <div class="form-group">
          <label for="name">Name</label>
          <input v-model="name" type="text" class="form-control" id="name">
        </div>
        <div class="form-group">
          <label for="description">Description</label>
          <input v-model="description" type="text" class="form-control" id="description">
        </div>
        <hr>
        <h3><b>Beta features</b> <button class="btn btn-success" @click.prevent="Curl">Test Curl Status</button></h3>
        <div class="form-group">
          <label for="url">URL to curl</label>
          <input v-model="url" type="text" class="form-control" id="url">
        </div>
        <div class="form-group">
          <label for="creds">HTTP Basic Credentials</label>
          <input v-model="creds" type="text" class="form-control" id="creds" placeholder="user:password">
        </div>
        <button class="btn btn-success" @click.prevent="Create">Create</button>
        <br>
      </div>
      <div class="col-lg-6">
        <img v-if="name" :src="robotHashUrl">
      </div>  
    </div>       
  </div>   
</template>
<script>
import axios from 'axios'
export default {
    data: function () {
      return {
        bots: undefined,
        name: "",
        description: "",
        error: undefined,
        success: undefined,
        creds: "",
        url:""
      }
    },
    computed: {
      robotHashUrl: function () {
        return "https://robohash.org/"+this.name
      }
    },
    methods: {
      Curl: function(){
        var that = this;
        axios.post("/api/v1/test_curl",{
            url: that.url,
            creds: that.creds,
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
      Create: function(){
        var that = this;
        axios.post("/api/v1/robots",{
            name: that.name,
            description: that.description,
            url: that.url,
            credentials: that.creds,
        },
        {withCredentials: true}).then(
          response => {
              that.error = undefined;
              if(response.data.status=="error"){
                  that.error = response.data.message;
              }
              else if(response.data.status=="success"){
                this.$router.push('/bots', () => {})
              }
          })
      }
    },
}
</script>