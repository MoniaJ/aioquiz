import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import swal from 'sweetalert2'

import router from './router'

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        session_uuid: null,
        language: 'pl',
        user: null
    },
    mutations: {
        authUser(state, session_uuid) {
            state.session_uuid = session_uuid;
        },
        storeUser(state, user) {
            state.user = user;
        },
        clearAuthData(state) {
            state.session_uuid = null;
            state.user = null;
        }
    },
    actions: {
        signup({commit, dispatch}, data) {
            axios.post('/users', data)
                .then(res => {
                    swal("Check Your e-mail", res.data.msg)
                })
        },
        login({commit, dispatch}, authData) {
            axios.post('/auth/login', {
                email: authData.email,
                password: authData.password,
            }).then((response) => {
                dispatch('loginUser', response.data)
            });
        },
        loginUser({commit, dispatch}, authData) {
            const now = new Date();
            const expirationDate = new Date(now.getTime() + 10000000 * 1000);
            localStorage.setItem('session_uuid', authData.session_uuid);
            localStorage.setItem('expirationDate', expirationDate);
            localStorage.setItem('user', JSON.stringify(authData));
            commit('storeUser', authData);
            commit('authUser', authData.session_uuid);
            router.replace('/lessons');
            dispatch('check_gdpr', authData);
        },
        tryAutoLogin({commit, dispatch}) {
            const session_uuid = localStorage.getItem('session_uuid');
            if (!session_uuid) {
                return
            }
            const expirationDate = localStorage.getItem('expirationDate');
            const user = JSON.parse(localStorage.getItem('user'));
            const now = new Date()
            if (now >= expirationDate) {
                return
            }
            commit('authUser', session_uuid);
            commit('storeUser', user);
            router.replace('/lessons');
            dispatch('check_gdpr', user);
        },
        logout({commit}) {
            const done = 0;
            axios.get('/auth/logout').then((resp) => {
                commit('clearAuthData');
                localStorage.removeItem('expirationDate');
                localStorage.removeItem('session_uuid');
                localStorage.removeItem('user');
                router.replace('/signin');
                swal("Log out", "You've been logged out successfully")
            })
        },
        storeUser({commit, state}, userData) {
            if (!state.session_uuid) {
                return
            }
            axios.post('/users', userData)
                .then(res => console.log(res))
        },
        fetchUser({commit, state}) {
            if (!state.session_uuid) {
                return
            }
            axios.get('/users')
                .then(res => {
                    const data = res.data;
                    const users = [];
                    for (let key in data) {
                        const user = data[key];
                        user.id = key;
                        users.push(user)
                    }
                    commit('storeUser', users[0]);
                })
        },
        check_gdpr({commit, dispatch}, authData) {
            if (authData.gdpr !== true) {
                const pl = 'I have read and accepted <a href="#/privacy_policy">Privacy Policy</a>';
                const en = 'Przeczytałem i akceptuję <a href="#/privacy_policy">Politykę Prywatności</a>';
                let html_text = authData.language === 'pl' ? pl : en;
                swal({
                    title: 'GDPR',
                    html: html_text,
                    showCancelButton: true,
                    confirmButtonText: 'Read&Agree',
                }).then((value) => {
                    let mtype = "error";
                    if (value.value) {
                        axios.get('/user/gdpr').then((response) => {
                            if (response.data.success) {
                                mtype = "success";
                                swal({
                                    text: response.data.msg,
                                    title: 'Privacy Policy Compliance',
                                    type: mtype,
                                    showConfirmButton: true,
                                    timer: 2000
                                });
                            } else {
                                dispatch('logout');
                            }
                        })
                    } else {
                        swal({
                            text: 'You have failed to comply with our Privacy Policy. You will be automatically logged out. Failing to comply by 25.05.2018 will lead to account removal.',
                            title: 'Privacy Policy Compliance',
                            type: mtype,
                            showConfirmButton: true,
                            timer: 10000
                        }).then((value) => {
                            dispatch('logout');
                        });
                    }
                })

            }
        }
    },
    getters: {
        user(state) {
            return state.user
        },
        isAuthenticated(state) {
            return state.session_uuid !== null
        },
        isSeated(state) {
            return state.user.seat !== null
        },
        sessionUUID(state) {
            return state.session_uuid
        },
        isAdmin(state) {
            if (state.user) {
                return state.user.admin
            }
            return false
        },
        isOrganiser(state) {
            if (state.user) {
                return state.user.organiser
            }
            return false
        },
        isMentor(state) {
            if (state.user) {
                return state.user.mentor
            }
            return false
        },
        userName(state) {
            if (state.user) {
                return state.user.name + ' ' + state.user.surname
            }
            return ''
        }
    }
})