<template>
	<div class="container">
		<h3>My Robots <router-link class="btn btn-success" :to="{ name: 'CreateBot' }">Create One</router-link></h3>
    <b v-if="bots==undefined || bots.length ==0">You don't have any robots.</b>
		<div class="container">
			<div class="row hidden-md-up">
				<div v-for="bot in bots" :key="bot.id" class="col-md-4">
					<div class="card" style="padding: 10px;">
						<div class="card-block">
							<img :src="robotHashUrl(bot.name)" class="card-img-top">
							<h4 class="card-title" style="text-align:center">{{ bot.name}}</h4>
							<p class="card-text p-y-1">{{ bot.description }}</p>
							<router-link class="btn btn-primary" style="width: 100%;" :to="{ name: 'Bot', params: { id: bot.id }}">View</router-link>
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
      }
    },
    methods: {
      robotHashUrl: function (name) {
        return "https://robohash.org/"+name
      }
    },
    mounted() {
        var that = this;
        axios.get("/api/v1/robots",{withCredentials: true})
        .then(
        response => {
            that.bots = response.data;
        })
    },
}
</script>