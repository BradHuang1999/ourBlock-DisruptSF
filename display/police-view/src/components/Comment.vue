<template>
    <div>
        <i>{{ comment.anonymous ? "anonymous" : comment.userId }}</i>
        <br>
        {{ comment.message }}
        <br>
        <br>
    </div>
</template>

<script>
export default {
    name: 'CommentComponent',

    props: ['comment']
}
</script>
