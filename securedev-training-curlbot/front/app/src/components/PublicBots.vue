<template>
	<div class="container">
    <div v-show="error" class="alert alert-danger" role="alert">
      {{ error }}
    </div>
		<h3>Search in Robots</h3>
    <form class="form-inline">
      <div class="form-group">
        <label for="inputPassword2" class="sr-only">Name</label>
        <input v-model="name" type="test" class="form-control" id="inputPassword2" placeholder="Name">
      </div>
      <button type="submit" @click.prevent="Search" class="btn btn-success" style="margin-left:10px">Search</button>
    </form>
		<div class="container">
			<div class="row hidden-md-up">
				<div v-for="bot in bots" :key="bot.id" class="col-md-4">
					<div class="card" style="padding: 10px;">
						<div class="card-block">
							<img :src="robotHashUrl(bot.name)" class="card-img-top">
							<h4 class="card-title" style="text-align:center">{{ bot.name}}</h4>
							<p class="card-text p-y-1">{{ bot.description }}</p>
						</div>
					</div>
				</div>
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
        name: undefined,
        error: undefined,
      }
    },
    methods: {
      robotHashUrl: function (name) {
        return "https://robohash.org/"+name
      },
      Search: function () {
        var that = this;
        axios.post("/api/v1/search",{
          name: that.name,
        },{withCredentials: true}).then(
        response => {
          that.error = undefined;
          if(response.data.status=="success")
            that.bots = response.data.message;
          else if (response.data.status=="error")
            that.error = response.data.message;
        })
      }
    },
}
</script>
