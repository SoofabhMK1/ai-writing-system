import api from './api'

const characterService = {
  getCharacters() {
    return api.get('/characters/')
  },
  createCharacter(characterData) {
    return api.post('/characters/', characterData)
  },
  getCharacterById(id) {
    return api.get(`/characters/${id}`)
  },
  deleteCharacter(id) {
    return api.delete(`/characters/${id}`)
  },
  // Update function is defined here for future use, but won't be implemented in the UI yet.
  updateCharacter(id, characterData) {
    return api.put(`/characters/${id}`, characterData)
  },
}

export default characterService
