import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);


const store = new Vuex.Store({
    state: {
        profile: {
            username: 'AnonymousUser',
            fullName: '?',
        }
    },
    actions: {
        LOAD_PROFILE: function ({ commit }) {
            bricks.get('/secured/projects').then((response) => {
                commit('SET_PROFILE', {list: response.data})
            }, (err) => {
                console.log(err)
            })
        }
    },
    mutations: {
        SET_PROFILE: (state, { profile }) => {
            state.profile = profile
        }
    },
    getters: {
        fullName: state => {
            var profile = state.profile;
            return profile.firstName + ' ' + profile.lastName;
        }
    },
    modules: {}
});

export default store