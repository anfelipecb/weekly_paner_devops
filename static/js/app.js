(function () {
  const addForm = document.getElementById("add-form");
  const formMessage = document.getElementById("form-message");
  const daySelect = document.getElementById("day");
  const titleInput = document.getElementById("title");

  function showMessage(text, isError) {
    formMessage.textContent = text;
    formMessage.className = "message " + (isError ? "error" : "success");
  }

  function renderTask(task) {
    const li = document.createElement("li");
    li.dataset.id = task.id;
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = task.completed;
    checkbox.setAttribute("aria-label", "Mark task completed");
    const span = document.createElement("span");
    span.className = "task-title" + (task.completed ? " done" : "");
    span.textContent = task.title;
    checkbox.addEventListener("change", function () {
      fetch("/api/tasks/" + task.id, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ completed: checkbox.checked }),
      })
        .then(function (r) {
          if (!r.ok) throw new Error("Update failed");
          span.classList.toggle("done", checkbox.checked);
        })
        .catch(function () {
          checkbox.checked = !checkbox.checked;
        });
    });
    li.appendChild(checkbox);
    li.appendChild(span);
    return li;
  }

  function loadTasks() {
    fetch("/api/tasks")
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        const lists = {};
        for (let d = 1; d <= 7; d++) {
          lists[d] = document.getElementById("day-" + d);
          lists[d].innerHTML = "";
        }
        (data.tasks || []).forEach(function (task) {
          const day = task.day_of_week;
          if (lists[day]) lists[day].appendChild(renderTask(task));
        });
      })
      .catch(function () {
        showMessage("Could not load tasks.", true);
      });
  }

  addForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const day = parseInt(daySelect.value, 10);
    const title = titleInput.value.trim();
    if (!title) return;
    formMessage.textContent = "";
    fetch("/api/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ day_of_week: day, title: title }),
    })
      .then(function (r) {
        return r.json().then(function (body) {
          if (!r.ok) throw new Error(body.error || "Failed");
          return body;
        });
      })
      .then(function (body) {
        showMessage("Task added.");
        titleInput.value = "";
        var list = document.getElementById("day-" + body.task.day_of_week);
        if (list) list.appendChild(renderTask(body.task));
      })
      .catch(function (err) {
        showMessage(err.message || "Could not add task.", true);
      });
  });

  loadTasks();
})();
