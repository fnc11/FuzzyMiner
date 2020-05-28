// Create by Eric Li at 28.05.20 for FuzzyMiner
const state = {
    id: null
};

const mutations = {
    SET_ID: (state, id) => {
      state.id = id;
    },
};

const actions = {
    setId({ commit }, id) {
        commit('SET_ID', id);
    },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
};