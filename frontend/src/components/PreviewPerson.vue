<template>
    <div class="preview">
        <loader v-if="isLoading" size="20"></loader>
        <template v-else>
            <p>{{ props.name }}, {{ props.firstName }}</p>
            <p>{{ props.email }}</p>
            <p>{{ props.organization.repr }}</p>
        </template>
    </div>
</template>

<script>
import Loader from './Loader'

import { getPerson } from '../ajax.js'

export default {
    name: 'PreviewPerson',
    components: {
        Loader,
    },
    props: {
        data: Object
    },
    data: function() {
        return {
            isLoading: true,
            props: {
                name: '',
                firstName: '',
                email: '',
                organization: {
                    repr: '',
                    data: { _id: null },
                }
            }
        }
    },
    created: function() {
        this.isLoading = true;

        if (this.data) {
            getPerson(this.data._id).then((person) => {
                this.props = person.data;
                this.isLoading = false;
            }, (result) => console.log(result));
        }
    },
}
</script>

<style>

</style>
