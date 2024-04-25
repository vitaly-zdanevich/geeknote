class Geeknote < Formula
  include Language::Python::Virtualenv

  desc "Command-line client for Evernote (without local cache - so you must be online to use it)"
  homepage 'https://github.com/vitaly-zdanevich/geeknote'
  head 'https://github.com/vitaly-zdanevich/geeknote.git'

  depends_on "python@3"

  resource "websocket-client" do
    url "https://files.pythonhosted.org/packages/a7/2b/0039154583cb0489c8e18313aa91ccd140ada103289c5c5d31d80fd6d186/websocket_client-0.40.0.tar.gz"
    sha256 "40ac14a0c54e14d22809a5c8d553de5a2ae45de3c60105fae53bcb281b3fe6fb"
  end

  resource "ipaddress" do
    url "https://files.pythonhosted.org/packages/4e/13/774faf38b445d0b3a844b65747175b2e0500164b7c28d78e34987a5bfe06/ipaddress-1.0.18.tar.gz"
    sha256 "5d8534c8e185f2d8a1fda1ef73f2c8f4b23264e8e30063feeb9511d492a413e1"
  end

  resource "orderedmultidict" do
    url "https://files.pythonhosted.org/packages/10/a5/a9596229782ffcb465f288588dff39ccd7f64fc453d64f75f5ef442315a8/orderedmultidict-0.7.11.tar.gz"
    sha256 "dc2320ca694d90dca4ecc8b9c5fdf71ca61d6c079d6feb085ef8d41585419a36"
  end

  resource "oauth2" do
    url "https://files.pythonhosted.org/packages/64/19/8b9066e94088e8d06d649e10319349bfca961e87768a525aba4a2627c986/oauth2-1.9.0.post1.tar.gz"
    sha256 "c006a85e7c60107c7cc6da1b184b5c719f6dd7202098196dfa6e55df669b59bf"
  end

  resource "httplib2" do
    url "https://files.pythonhosted.org/packages/e4/2e/a7e27d2c36076efeb8c0e519758968b20389adf57a9ce3af139891af2696/httplib2-0.10.3.tar.gz"
    sha256 "e404d3b7bd86c1bc931906098e7c1305d6a3a6dcef141b8bb1059903abb3ceeb"
  end

  resource "evernote" do
    url "https://files.pythonhosted.org/packages/3b/8e/dba34913e7dbccd868cdf228c5104f97ad97d4618994f0c5dd456496ae81/evernote-1.25.2.tar.gz"
    sha256 "69212c161e2538db13dd34e749125ff970f6c88aaa5f52f6925ffcf883107302"
  end

  resource "html2text" do
    url "https://files.pythonhosted.org/packages/22/c0/2d02a1fb9027f54796af2c2d38cf3a5b89319125b03734a9964e6db8dfa0/html2text-2016.9.19.tar.gz"
    sha256 "554ef5fd6c6cf6e3e4f725a62a3e9ec86a0e4d33cd0928136d1c79dbeb7b2d55"
  end

  resource "SQLAlchemy" do
    url "https://files.pythonhosted.org/packages/02/69/9473d60abef55445f8e967cfae215da5de29ca21b865c99d2bf02a45ee01/SQLAlchemy-1.1.9.tar.gz"
    sha256 "b65cdc73cd348448ef0164f6c77d45a9f27ca575d3c5d71ccc33adf684bc6ef0"
  end

  resource "markdown2" do
    url "https://files.pythonhosted.org/packages/2f/c0/6da6f0caec68c99dd4bd4661b0ac16a50bdad89b1bbeb5a40686826762dc/markdown2-2.3.3.zip"
    sha256 "20a9439a80d93c221080297119d9d31285a18c904489948deae3c7e05c7c5e38"
  end

  resource "beautifulsoup4" do
    url "https://files.pythonhosted.org/packages/9b/a5/c6fa2d08e6c671103f9508816588e0fb9cec40444e8e72993f3d4c325936/beautifulsoup4-4.5.3.tar.gz"
    sha256 "b21ca09366fa596043578fd4188b052b46634d22059e68dd0077d9ee77e08a3e"
  end

  resource "thrift" do
    url "https://files.pythonhosted.org/packages/a3/ea/84a41e03f1ab14fb314c8bcf1c451090efa14c5cdfb9797d1079f502b54e/thrift-0.10.0.zip"
    sha256 "b7f6c09155321169af03f9fb20dc15a4a0c7481e7c334a5ba8f7f0d864633209"
  end

  resource "future" do
    url "https://files.pythonhosted.org/packages/00/2b/8d082ddfed935f3608cc61140df6dcbf0edea1bc3ab52fb6c29ae3e81e85/future-0.16.0.tar.gz"
    sha256 "e39ced1ab767b5936646cedba8bcce582398233d6a627067d4c6a454c90cfedb"
  end

  # for proxyenv
  resource "docker-py" do
    url "https://files.pythonhosted.org/packages/fa/2d/906afc44a833901fc6fed1a89c228e5c88fbfc6bd2f3d2f0497fdfb9c525/docker-py-1.10.6.tar.gz"
    sha256 "4c2a75875764d38d67f87bc7d03f7443a3895704efc57962bdf6500b8d4bc415"
  end

  resource "htpasswd" do
    url "https://files.pythonhosted.org/packages/b9/2f/8b76f8b77125b75c3532966f3291f9e8787268be65fc4c9694887cba9375/htpasswd-2.3.tar.gz"
    sha256 "565f0b647a32549c663ccfddd1f501891daaf29242bbc6174bdd448120383e3d"
  end

  resource "proxyenv" do
    url "https://files.pythonhosted.org/packages/69/98/46baccf9ce353828726e0d302dad201e634fe4b50f6f61891f0721f40789/proxyenv-0.5.1.tar.gz"
    sha256 "e73caf8b063b7fbfb93b67e725a71469768262a9dddb4d9dfb79bb1e84cab4b9"
  end

  resource "lxml" do
    url "https://files.pythonhosted.org/packages/39/e8/a8e0b1fa65dd021d48fe21464f71783655f39a41f218293c1c590d54eb82/lxml-3.7.3.tar.gz"
    sha256 "aa502d78a51ee7d127b4824ff96500f0181d3c7826e6ee7b800d068be79361c7"
  end

  resource "backports.ssl_match_hostname" do
    url "https://files.pythonhosted.org/packages/76/21/2dc61178a2038a5cb35d14b61467c6ac632791ed05131dda72c20e7b9e23/backports.ssl_match_hostname-3.5.0.1.tar.gz"
    sha256 "502ad98707319f4a51fa2ca1c677bd659008d27ded9f6380c79e8932e38dcdf2"
  end

  resource "docker-pycreds" do
    url "https://files.pythonhosted.org/packages/95/2e/3c99b8707a397153bc78870eb140c580628d7897276960da25d8a83c4719/docker-pycreds-0.2.1.tar.gz"
    sha256 "93833a2cf280b7d8abbe1b8121530413250c6cd4ffed2c1cf085f335262f7348"
  end

  resource "requests" do
    url "https://files.pythonhosted.org/packages/16/09/37b69de7c924d318e51ece1c4ceb679bf93be9d05973bb30c35babd596e2/requests-2.13.0.tar.gz"
    sha256 "5722cd09762faa01276230270ff16af7acf7c5c45d623868d9ba116f15791ce8"
  end

  resource "six" do
    url "https://files.pythonhosted.org/packages/b3/b2/238e2590826bfdd113244a40d9d3eb26918bd798fc187e2360a8367068db/six-1.10.0.tar.gz"
    sha256 "105f8d68616f8248e24bf0e9372ef04d3cc10104f1980f54d57b2ce73a5ad56a"
  end

  def install
    virtualenv_install_with_resources

    bash_completion.install "completion/bash_completion/_geeknote" => "geeknote"
    zsh_completion.install "completion/zsh_completion/_geeknote" => "_geeknote"
  end

  test do
    system "py.test"
  end
end
