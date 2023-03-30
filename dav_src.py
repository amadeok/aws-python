print("hello test 6")

resolve = app.GetResolve()
projectManager = resolve.GetProjectManager()
proj = projectManager.CreateProject("new proj")


print(proj)