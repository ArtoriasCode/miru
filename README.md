# 🔥 Miru
With Miru, you can create your own browser-based applications. It allows you to call Python code directly from Vue and vice versa, enabling you to combine convenient reactive Vue layout and business logic processing in Python.

The main features you will get when using Miru:
- ✏️ Vue syntaxis.
- ➡️ Calling Python code from JavaScript.
- ⬅️ Calling JavaScript code from Python.
- 🌐 Application as a web page.

> [!IMPORTANT]
> The repository contains [examples](https://github.com/ArtoriasCode/miru/tree/main/examples) of simple applications.

## 🌐 Supported browsers
> [!NOTE]
> Perhaps there aren't as many as you would like yet, but I will try to add more in the future.

There are currently three browsers available for you to choose from. All you need is for them to be available in the system, and Miru will find the installation path itself.

|          | MacOS  | Windows | Linux  |
|----------|--------|---------|--------|
| Chrome   | ✅     | ✅      | ✅     |
| Chromium | ✅     | ✅      | ✅     |
| Edge     | ✅     | ✅      | ✅     |

## 📚 Packages
> [!NOTE]
> Miru uses only the minimum set of tools necessary so as not to burden your applications with unnecessary dependencies.

List of packages used to create Miru:
- **[Vue](https://github.com/vuejs/core)**: Vue.js is a progressive, incrementally-adoptable JavaScript framework for building UI on the web. 
- **[Bottle](https://pypi.org/project/bottle/)**: Fast and simple WSGI-framework for small web-applications.
- **[Bottle websocket](https://pypi.org/project/bottle-websocket/)**: WebSockets for bottle.

## 🔨 Installation
1) Install Miru on your device:
```
pip install git+https://github.com/ArtoriasCode/miru.git
```
2) Create a new project using [Vue CLI](https://cli.vuejs.org/#getting-started):
```
vue create frontend
```
3) Configure your project for compatibility with Miru:
```
python -m miru setup --vue-dir frontend
```
4) Your project is now integrated with Miru. You can layout your application as you would a regular Vue website.

## 🔍 Usage example
> [!TIP]
> This is just a minimal example. You can build full-fledged applications, just as you would build websites on Vue.

An example of text reversing using Python.

Example of modified content in a standard template `frontend/src/components/HelloWorld.vue`:
```vue
<template>
  <div class="reverser">
    <form @submit.prevent="reverseValue">
      <input
          type="text"
          v-model="text"
          placeholder="Enter text"
      />
      <button type="submit">Reverse</button>
    </form>
    <p v-if="reversed">Reversed: <strong>{{ reversed }}</strong></p>
  </div>
</template>

<script setup>
import {ref} from 'vue';

const miru = window.miru;
const text = ref('');
const reversed = ref('');

async function reverseValue() {
  await miru.call_py("reverse_value", text.value);
}

miru.listen("output_reverse", (value) => {
  reversed.value = value;
});
</script>

<style scoped>
.reverser {
  max-width: 300px;
  margin: 2rem auto;
}

input {
  padding: 0.4rem;
  margin-right: 0.5rem;
}

button {
  padding: 0.4rem 0.8rem;
}
</style>
```

Example `main.py` in the root directory (same location as the `frontend` directory):
```python
from miru import init, start, listen, call_js, BrowsersEnum


@listen
def reverse_value(value: str) -> None:
    """
    Reverses the specified text and calls the output_reverse function in your application's JavaScript.
    
    Parameters:
    - value: The text to reverse.
    
    Returns:
    - None.
    """
    reversed_value = value[::-1]
    call_js("output_reverse", reversed_value)

if __name__ == '__main__':
    init(mode=BrowsersEnum.CHROME)
    start()
```