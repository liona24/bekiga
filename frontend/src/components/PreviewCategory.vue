<template>
    <div class="preview">
        <loader v-if="isLoading" size="20"></loader>
        <template v-else>
            <p>{{ props.name }}</p>
            <ul>
                <li v-for="(std, i) in props.inspectionStandards" :key="'inspStd' + i">
                    {{ std.repr }}
                </li>
            </ul>
        </template>
    </div>
</template>

<script>
import Loader from './Loader'

import { getCategory } from '../ajax.js'

export default {
    name: 'PreviewCategory',
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
                inspectionStandards: [],
            }
        }
    },
    created: function() {
        this.isLoading = true;

        if (this.data) {
            getCategory(this.data._id).then((res) => {
                this.props = res.data;
                this.isLoading = false;
            }, (result) => console.error(result));
        }
    },
}
</script>

<style>

</style>