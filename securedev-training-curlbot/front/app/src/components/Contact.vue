<template>
    <div>
      <a class="hiddenanchor" id="signup"></a>
      <a class="hiddenanchor" id="signin"></a>

      <div class="login_wrapper">
        <div class="animate form login_form">
          <section class="login_content">
            <form>
              <h1>Contact us</h1>
              <div v-show="error" class="alert alert-danger" role="alert">
                {{ error }}
              </div>
              <div v-show="success" class="alert alert-success" role="alert">
                {{ success }}
              </div>
              
              <div>
                <input v-model="name" type="text" class="form-control" placeholder="Name" required="" />
              </div>
              <br>
              <div>
                <input v-model="email" type="email" class="form-control" placeholder="Email" required="" />
              </div>
              <br>
              <div>
                <textarea v-model="content" type="test" class="form-control" placeholder="Content" required=""></textarea>
              </div>
              <br>
              <div>
                <button type="button" class="btn btn-success" @click.prevent="Contact">Send us a message !</button>
              </div>

              <div class="clearfix"></div>
            </form>
          </section>
        </div>
      </div>
    </div>
</template>
<script>
import axios from 'axios'
import store from '../store/AuthenticationStore'
export default {
    store: store,
    data: function () {
      return {
        name: undefined,
        email: undefined,
        content: undefined,
        error: undefined,
        success: undefined,
      }
    },
    methods: {
        Contact(){
            if(this.name && this.email && this.content){
                var that = this;
                axios.post("/api/v1/contact",
                {
                    name: that.name,
                    email: that.email,
                    content: that.content,
                },{withCredentials: true}).then(
                response => {
                    that.error = undefined;
                    that.success = undefined;
                    if(response.data.status=="error"){
                        that.error = response.data.message;
                    }
                    else if(response.data.status=="success"){
                        that.success = response.data.message;
                    }
                });
        }
      }
    }
}
</script>
