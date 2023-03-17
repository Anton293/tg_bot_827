using System.Net;
using System.Reflection;
using System.Threading.Tasks;

public override async Task Execute(Service service)
{
    WebClient webClient = new WebClient();
    string codeUrl = "https://example.com/mycode.cs";
    string code = await webClient.DownloadStringTaskAsync(codeUrl);

    Assembly assembly = Assembly.Load(code);
    MethodInfo method = assembly.GetType("MyCodeClass").GetMethod("MyCodeMethod");
    method.Invoke(null, null);
}
