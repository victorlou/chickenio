import Card from "../components/card"

const GlobalComponents = {
    install(Vue) {
        Vue.component(Card.name, Card);
    }
}

export default GlobalComponents;